"""
fleet_stt_client — thin client for the fleet-stt service (OW-698 capability extraction).

tldv_downloader's README roadmap funds "Whisper transcription". Instead of bundling
its own Whisper, tldv calls the fleet's standalone multi-provider STT service
(Deepgram/Whisper/Gemini + fallback + circuit-breaker + durable queue). This is the
consumer side of the soft_leverage[fleet-stt] edge.

Design canon: platform-docs/docs/specs/2026-06-29-fleet-stt-extraction.md
Service: vagary-voice/fleet-stt/ (tailnet HTTP; PLANNED — deploy-gated).

Two call shapes (mirroring the service's audio-input contract):
  * transcribe_file()  — small/medium local audio → sync inline base64 (one round-trip).
  * transcribe_url()   — large or already-hosted audio → async job + poll.

No SDK dependency beyond `requests` (already a tldv dep). The service token + base URL
come from the environment (FLEET_STT_URL / FLEET_STT_TOKEN) — never hardcoded.
"""
from __future__ import annotations

import base64
import os
import time
from dataclasses import dataclass
from typing import Optional

import requests


@dataclass
class Transcript:
    transcription_id: str
    status: str
    text: Optional[str]
    provider_used: Optional[str]
    confidence: Optional[float]
    language: Optional[str]
    duration_seconds: Optional[float]


class FleetSttError(RuntimeError):
    pass


class FleetSttClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        token: Optional[str] = None,
        organization_id: str = "tldv",
        timeout: int = 180,
    ):
        self.base_url = (base_url or os.environ.get("FLEET_STT_URL", "")).rstrip("/")
        self.token = token or os.environ.get("FLEET_STT_TOKEN", "")
        self.organization_id = organization_id
        self.timeout = timeout
        if not self.base_url:
            raise FleetSttError("FLEET_STT_URL not set (the tailnet URL of the fleet-stt service)")
        if not self.token:
            raise FleetSttError("FLEET_STT_TOKEN not set (the service bearer token)")

    @property
    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    @staticmethod
    def _to_transcript(j: dict) -> Transcript:
        return Transcript(
            transcription_id=j.get("transcription_id", ""),
            status=j.get("status", "unknown"),
            text=j.get("transcript"),
            provider_used=j.get("provider_used"),
            confidence=j.get("confidence"),
            language=j.get("language"),
            duration_seconds=j.get("duration_seconds"),
        )

    def transcribe_file(
        self, path: str, content_type: str = "audio/wav", language: Optional[str] = None
    ) -> Transcript:
        """Sync inline transcription of a local audio file (one round-trip).

        Use for clips under the service's STT_MAX_AUDIO_BYTES (default 25 MiB). For
        larger meetings, host the audio and use transcribe_url() instead.
        """
        with open(path, "rb") as fh:
            audio_b64 = base64.b64encode(fh.read()).decode("ascii")
        body = {
            "organization_id": self.organization_id,
            "audio_base64": audio_b64,
            "content_type": content_type,
        }
        if language:
            body["language"] = language
        resp = requests.post(
            f"{self.base_url}/v1/transcribe", json=body, headers=self._headers, timeout=self.timeout
        )
        if resp.status_code == 413:
            raise FleetSttError("audio too large for inline path — use transcribe_url()")
        if resp.status_code != 200:
            raise FleetSttError(f"transcribe failed [{resp.status_code}]: {resp.text[:200]}")
        return self._to_transcript(resp.json())

    def transcribe_url(
        self,
        audio_url: str,
        content_type: str = "audio/mp4",
        language: Optional[str] = None,
        poll_interval: float = 2.0,
        max_wait: float = 600.0,
    ) -> Transcript:
        """Async transcription of a hosted audio URL (the service fetches it, SSRF-guarded).

        Ideal for long meetings: tldv already resolves a public CDN media URL — pass it
        directly so the bytes never round-trip through this client.
        """
        body = {
            "organization_id": self.organization_id,
            "audio_url": audio_url,
            "content_type": content_type,
        }
        if language:
            body["language"] = language
        resp = requests.post(
            f"{self.base_url}/v1/transcribe", json=body, headers=self._headers, timeout=self.timeout
        )
        if resp.status_code not in (200, 202):
            raise FleetSttError(f"enqueue failed [{resp.status_code}]: {resp.text[:200]}")
        job_id = resp.json()["transcription_id"]

        deadline = time.monotonic() + max_wait
        while time.monotonic() < deadline:
            status = self.get(job_id)
            if status.status in ("succeeded", "failed", "dead_letter"):
                if status.status != "succeeded":
                    raise FleetSttError(f"transcription {status.status}: {job_id}")
                return status
            time.sleep(poll_interval)
        raise FleetSttError(f"transcription timed out after {max_wait}s: {job_id}")

    def get(self, transcription_id: str) -> Transcript:
        resp = requests.get(
            f"{self.base_url}/v1/transcribe/{transcription_id}",
            headers=self._headers,
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise FleetSttError(f"status lookup failed [{resp.status_code}]: {resp.text[:200]}")
        return self._to_transcript(resp.json())
