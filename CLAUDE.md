# tldv_downloader — CLAUDE.md v2

**Date:** 2026-04-28 (S11B authoring)
**Supersedes:** v1 (commit-sha pending S11C verification)
**Tier:** C (stable utility) — sponsor-ready OSS

## Claude Preamble
<!-- VERSION: 2026-06-04-v52 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws (§1–§55) load via user-level `~/.claude/conventions/` and are ALWAYS in context** — `universal-claudemd.summary.md` (≤50-line salient view, read FIRST) → `universal-claudemd.md` (full) + `project-hygiene.md`. Do **NOT** assume their content from memory; consult + verify before asserting (§34 / §43.6 / §43.7). The `## Active Cluster Playbooks` block below names this repo's situational playbooks **read-on-demand** (§49.10): Read the named playbook when its trigger fires — never guess its contents; always-load guardrails are inline. Sync: `~/.claude/scripts/sync-preambles.py` (manual cadence; run after any source edit).

## Active Cluster Playbooks (read-on-demand — §49.10; bodies at ~/.claude/conventions/playbooks/)
<!-- BEGIN PLAYBOOKS BLOCK (managed by sync-preambles.py — read-on-demand pointers per §49.10; bodies at ~/.claude/conventions/playbooks/) -->

These cluster playbooks apply to this repo. You do NOT know their contents from memory —
**Read the named file when its trigger fires; never assume** (§49.10, §34, §43.6). Bodies are
NOT inlined and NOT @-imported; the always-load GUARDRAILs below are the only parts that must
hold without a Read.

- `commercial-bound.md` — when: license / sponsor-readiness / graph-tool-output / white-label work. GUARDRAIL: never commit/ship GitNexus (PolyForm-NC) graph output from a commercial-bound repo — CGC is the canonical graph source.
- `multi-lang.md` — when: cross-language refactor / rename spanning two or more languages.
- `brand-registry.md` — when: brand / positioning / brand-canon / cross-repo brand work.

<!-- END PLAYBOOKS BLOCK -->

## Identity & Role

`tldv_downloader` is a **cross-platform Python utility** that exports tldv.io meeting recordings to local MP4 via HLS stream capture (single or batch, parallel, resumable). Public Cramraika org repo (13★ / 4 forks); MIT; FUNDING.yml live. **Unarchived 2026-04-19** to accept sponsorships + light maintenance.

Vagary Labs brand: **OSS Utilities** (sponsor-ready).

## Coverage Today (post-PCN-S6/S7/S11A)

Per matrix row `tldv-downloader`:

```
Mail | DNS | RP | Orch | Obs | Backup | Sup | Sec | Tun | Err | Wflw | Spec
 NA  | NA  | NA | NA   | NA  | NA     | T   | U   | NA  | NA  | NA   | NA
```

- USED: Sec (`.env` denied by `.claude/settings.json`; CodeQL on push + weekly Mon 03:30 UTC; SECURITY.md present).
- TRIGGER-TO-WIRE: Sup (Cosign post-PR-#50 — applies to release artefacts if/when packaged for distribution).
- NA across all other dimensions — local CLI utility; no VPS deploy, no telemetry, no network surface.

## What's Wired

- **GitHub:** `Cramraika/tldv_downloader` (public, unarchived 2026-04-19); FUNDING.yml live; sponsor link in README + CLAUDE.md.
- **CI:** GitHub Actions on `ubuntu-latest` Python 3.11 — flake8 (E9,F63,F7,F82) + import verify + pip-audit (non-blocking) + markdown summary. **GREEN.**
- **CodeQL** on push + weekly Mon 03:30 UTC.
- **Renovate + Dependabot** automated dep bumps.

## Stack

- **Runtime:** Python 3.7+ (single-file `tldv_downloader.py`, 526 lines)
- **HTTP:** `requests` (pinned)
- **Download tools:** N_m3u8DL-RE (preferred, HLS-aware) or FFmpeg (fallback)
- **Parallelism:** `concurrent.futures.ThreadPoolExecutor`

## Roadmap (post-S11A) — sponsor-funded (held until sponsorship materializes)

### Cluster 3 — Cosign per-repo CI fanout
- T (post host_page PR #50 merge); applies to release artefacts (e.g., GitHub Release `.zip` bundles or PyPI sdist if packaged).

### Existing roadmap (carried forward)
- **Whisper transcription** — auto-transcribe downloaded MP4s.
- **Obsidian export** — write meeting notes + links into Obsidian vault.
- **UI wrapper** — GUI for non-CLI users (Tauri or Electron candidate).
- **Maintenance floor:** keep up with tldv.io API drift + CVE bumps.

## ADR Compliance

- **ADR-038 personal-scope:** ✓ — Cramraika org public; MIT.
- **ADR-033 Renovate canonical:** ✓ — Renovate active.
- **ADR-041 Trivy gate:** T (post-Cosign-fanout if container distribution added; today it's a single-file Python script).
- **SOC2 risk-register cross-ref:** N/A (no customer data; user provides own auth token interactively).

## Cross-references

- `platform-docs/05-architecture/part-B-service-appendices/products/tldv-downloader.md` (or specialized tier; pending S11B authoring)
- `~/.claude/conventions/universal-claudemd.md` §41 brand architecture (OSS Utilities)
- `~/.claude/conventions/repo-inventory.md`

## Migration from v1

**Major v1 → v2 changes:**
1. Per-project-service-matrix row added (USED for Sec; T for Sup; NA elsewhere).
2. Cluster 3 Cosign per-repo CI fanout queued post-PR-#50.
3. Unarchive timeline (2026-04-19) reaffirmed.
4. host_page-fork-template candidate (per host_page CLAUDE.md fork-targets) — first product landing-page fork for `tldv.<TLD>` could leverage host_page Tier-A design.
