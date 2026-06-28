# Transcription via fleet-stt (roadmap integration)

**Status:** integration design + reference client. **NOT merged** (branch `feat/fleet-stt-integration`).
**Why:** the README roadmap funds "Whisper transcription". Rather than bundle a Whisper
dependency, tldv_downloader consumes the fleet's standalone **fleet-stt** service
(multi-provider STT: Deepgram → Whisper → Gemini fallback, durable queue, circuit-breaker).

This is the consumer side of the **OW-698** capability-extraction edge
`tldv-downloader.soft_leverage[fleet-stt]`.
Service + design canon: `vagary-voice/fleet-stt/` · `platform-docs/docs/specs/2026-06-29-fleet-stt-extraction.md`.

## How it wires in

1. tldv downloads a meeting recording (existing flow → an `.mp4`/audio file, or a resolved CDN media URL).
2. With `--transcribe`, tldv calls fleet-stt:
   - **small/medium local file** → `transcribe_file()` (sync inline base64, one round-trip);
   - **long meeting / hosted media** → `transcribe_url()` (async job; fleet-stt fetches the URL, SSRF-guarded, and tldv polls).
3. The transcript is written next to the video (e.g. `<name>.transcript.txt`) — fulfilling the roadmap item without any STT code or provider key in this repo.

```python
from fleet_stt_client import FleetSttClient   # env: FLEET_STT_URL, FLEET_STT_TOKEN

stt = FleetSttClient(organization_id="tldv")

# small clip already on disk:
t = stt.transcribe_file("meeting.m4a", content_type="audio/m4a")
print(t.provider_used, t.text)

# long meeting via the already-resolved public CDN URL (no local round-trip):
t = stt.transcribe_url(cdn_media_url, content_type="audio/mp4")
open("meeting.transcript.txt", "w").write(t.text or "")
```

## Why this is the right shape

- **No provider lock-in / no key in tldv** — fleet-stt resolves Deepgram/Whisper/Gemini keys server-side; tldv only holds the fleet service token (`FLEET_STT_TOKEN`, env, never committed).
- **Resilience for free** — provider fallback + per-provider circuit-breaker + durable retry live in the service; a single provider outage doesn't fail a transcription.
- **Long-audio safe** — the async URL path means multi-hour meetings never base64-round-trip through the CLI; fleet-stt streams the fetch (size-capped, rebinding-safe).

## Cutover (gated)

Merging this branch is **step 6 of the fleet-stt cutover** (spec §8) and is **operator-gated**: it only lands after fleet-stt is deployed + health-checked on compute-1 and `FLEET_STT_URL`/`FLEET_STT_TOKEN` are provisioned. Until then this branch is the documented, ready integration — not merged.

The wiring into `tldv_downloader.py` (a `--transcribe` flag calling `fleet_stt_client`) is a small, additive follow-up applied at cutover; the reference client (`fleet_stt_client.py`) is complete and standalone.
