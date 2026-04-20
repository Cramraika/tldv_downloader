# TLDV Downloader

## Claude Preamble
<!-- VERSION: 2026-04-19-v12 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws** (§4), **MCP routing** (§6), **Drift protocol** (§11), **Dynamic maintenance** (§14), **Capability resolution** (§15), **Subagent SKILL POLICY** (§16), **Session continuity** (§17), **Decision queue** (§17.a), **Attestation** (§18), **Cite format** (§19), **Three-way disagreement** (§20), **Pre-conditions** (§21), **Provenance markers** (§22), **Redaction rules** (§23), **Token budget** (§24), **Tool-failure fallback** (§25), **Prompt-injection rule** (§26), **Append-only discipline** (§27), **BLOCKED_BY markers** (§28), **Stop-loss ladder** (§29), **Business-invariant checks** (§30), **Plugin rent rubric** (§31), **Context ceilings** (§32), **Doc reference graph** (§33), **Anti-hallucination** (§34), **Past+Present+Future body** (§35), **Project trackers** (§36), **Doc ownership** (§37), **Archive-on-delete** (§38), **Sponsor + white-label** (§39), **Doc-vs-code drift** (§40), **Brand architecture** (§41), **Design system integration** (§42).

**Sources**: `~/.claude/conventions/universal-claudemd.md` (laws, MCP routing, lifecycle, rent rubric, doc-graph, anti-hallucination, brand architecture) + `~/.claude/conventions/project-hygiene.md` (doc placement, cleanup, archive-on-delete, ownership matrix) + `~/.claude/conventions/design-system.md` (per-repo Tier A/B/C design posture, Stitch wiring). Read relevant sections before significant work. Re-audit due **2026-07-19**. Sync: `~/.claude/scripts/sync-preambles.py`.

## One-liner
Cross-platform Python utility that exports tldv.io meeting recordings to local MP4 via HLS stream capture -- single or batch, parallel, resumable.

## References
- Universal laws: `~/.claude/conventions/universal-claudemd.md`
- Project hygiene: `~/.claude/conventions/project-hygiene.md`
- Environments: `docs/ENVIRONMENTS.md`
- Upstream (HLS tool): https://github.com/nilaoda/N_m3u8DL-RE
- GitHub: https://github.com/Cramraika/tldv_downloader (public, 13★/4 forks, unarchived 2026-04-19)
- Sponsors: https://github.com/sponsors/Cramraika

## Status & Tier
- **Tier: C (stable utility)** -- single-file script, feature-complete for current scope
- **Sponsor-ready OSS** -- public, FUNDING.yml live, README relaunched with sponsor CTA (commit `ebfbee7`)
- Repo was archived and was just **unarchived on 2026-04-19** to accept sponsorships + light maintenance

## Products

| Product | What It Does | Who Uses It | Status |
|---------|-------------|-------------|--------|
| Single Meeting Downloader | Downloads one TLDV meeting recording by URL using HLS stream capture | OSS users + developer | Stable |
| Batch Downloader | Parallel downloads of multiple meeting recordings from a list of URLs | OSS users + developer | Stable |

### Single Meeting Downloader
- **User journey**: Get auth token from tldv.io browser session (Network tab) -> Run script with meeting URL -> Script fetches meeting metadata from TLDV API -> Extracts HLS stream URL -> Downloads via N_m3u8DL-RE or FFmpeg -> Saves as MP4 with sanitized filename (includes meeting title + date)
- **Success signals**: Meeting video saved locally within minutes; metadata JSON alongside
- **Failure signals**: Auth token expired (401); HLS stream URL format drift; download tool missing from PATH

### Batch Downloader
- **User journey**: Prepare list of meeting URLs -> Run in batch mode -> ThreadPoolExecutor downloads in parallel (1-8 workers) -> Per-download progress -> All files saved to chosen directory
- **Success signals**: All meetings downloaded without babysitting; no partial/corrupt files
- **Failure signals**: Silent per-download failures; parallel workers saturate network; duplicate downloads

## Active Role-Lanes
- **Engineer** (primary) -- Python maintenance, CVE bumps, upstream API drift fixes
- **Writer / Marketer** (secondary) -- README positioning, sponsor CTA copy, changelog on release
- **Support** (ad-hoc) -- triage issues from public users (13★, 4 forks -- real inbound expected)

## Stack
- **Runtime**: Python 3.7+ (single-file: `tldv_downloader.py`, 526 lines)
- **HTTP**: `requests` (pinned via `requirements.txt`)
- **Download tools**: N_m3u8DL-RE (preferred, HLS-aware, parallel segments) or FFmpeg (fallback)
- **Parallelism**: `concurrent.futures.ThreadPoolExecutor`

## Build / Test / Deploy
```bash
# Install
pip install -r requirements.txt

# Run
python tldv_downloader.py              # Interactive (single or batch)
python tldv_downloader.py --help       # Auth-token instructions
```
No deployment -- local CLI only. Distribution is the repo + README.

## Key Directories
- `tldv_downloader.py` -- main script (single-file architecture)
- `requirements.txt` -- sole Python dependency
- `.github/` -- `ci.yml`, `codeql.yml`, `renovate.yml`, `FUNDING.yml`, ISSUE_TEMPLATE, CODEOWNERS, PR template, dependabot
- `docs/ENVIRONMENTS.md` -- setup + troubleshooting for end-users
- `.claude/settings.json` -- project-scoped plugin profile

## Dependency Graph
- **Upstream (runtime, external)**: `tldv.io` API (`gw.tldv.io/v1/meetings/{id}/watch-page`), HLS/m3u8 stream endpoints, `N_m3u8DL-RE` CLI, FFmpeg CLI
- **Upstream (library)**: `requests` only
- **Downstream**: personal archival / OSS users downloading own meetings; no programmatic consumers

## Roadmap (sponsor-funded)
From README sponsor CTA -- held until sponsorship materializes:
- **Whisper transcription** -- auto-transcribe downloaded MP4s
- **Obsidian export** -- write meeting notes + links into an Obsidian vault
- **UI wrapper** -- GUI for non-CLI users (Tauri or Electron candidate)
- **Maintenance floor**: keep up with tldv.io API drift + CVE bumps

## Observability
**n/a** -- local CLI utility. No telemetry, no error reporting, no metrics. If a VPS deployment is ever added, the stack in § External Services below applies.

## Security & Secrets
- **No envs required at runtime** -- auth token is prompted interactively from the user (copy-paste from browser Network tab)
- Never hardcode tokens in the script or in URL-list files
- `.env` / `.env.*` denied by `.claude/settings.json`
- `SECURITY.md` present -- report via `chinu.ramraika@gmail.com`
- CodeQL scan runs on push + weekly (Monday 03:30 UTC)

## Deployment Environments
- **Local only** -- no staging, no prod. End-users clone + run.
- **CI**: GitHub Actions on `ubuntu-latest` / Python 3.11 -- flake8 (E9,F63,F7,F82) + import verify + `pip-audit` (non-blocking) + markdown summary

## External Services (MCPs, integrations)
- **GitHub Sponsors** -- FUNDING.yml live; sponsor link in README + CLAUDE.md
- **n8n** (`https://n8n.chinmayramraika.in`) -- optional webhook integration wired via `N8N_WEBHOOK_URL` + `N8N_API_KEY` envs (not used by current script; reserved for future workflow triggers)
- **Renovate + Dependabot** -- automated dep bumps
- **GitHub Issues + Discussions** -- primary support surface

## Past (recent history)
- **2026-04-19** -- repo unarchived; FUNDING.yml added; README relaunched with sponsor CTA + Who-is-this-for + social proof badges (commit `ebfbee7`)
- **2026-04-13 -> 04-18** -- hygiene sweep (CODEOWNERS, PR template, SECURITY.md, issue templates, CodeQL, Dependabot, Renovate)
- **2026-04-06** -- requests 2.32.5 -> 2.33.0 (CVE bump)
- **2026-03** -- CI pipeline upgraded to ASM quality standard; flake8 + pip-audit
- Original script committed 2025; current feature set stable since.

## Known Limitations
- Auth token expires with browser session -- no refresh flow
- HLS URL format is reverse-engineered; tldv.io server change may break the extractor until patched
- No resume-from-partial for a single file (only batch-level resume by rerunning)
- No tests -- script is interactive; coverage would require mocking the full TLDV auth+HLS flow

## Deviations from Universal Laws
None. Standard hygiene applies: no hardcoded secrets, conventional commits, no `--no-verify`, destructive ops require explicit user sign-off, append-only changelog via git history (no `CHANGELOG.md` since no tagged releases yet).
