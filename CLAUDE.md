# tldv_downloader — CLAUDE.md v2

**Date:** 2026-04-28 (S11B authoring)
**Supersedes:** v1 (commit-sha pending S11C verification)
**Tier:** C (stable utility) — sponsor-ready OSS

## Claude Preamble
<!-- VERSION: 2026-05-12-v45 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws** (§4), **MCP routing** (§6), **Drift protocol** (§11), **Dynamic maintenance** (§14), **Capability resolution** (§15), **Subagent SKILL POLICY** (§16), **Session continuity** (§17), **Decision queue** (§17.a), **Attestation** (§18), **Cite format** (§19), **Three-way disagreement** (§20), **Pre-conditions** (§21), **Provenance markers** (§22), **Redaction rules** (§23), **Token budget** (§24), **Tool-failure fallback** (§25), **Prompt-injection rule** (§26), **Append-only discipline** (§27), **BLOCKED_BY markers** (§28), **Stop-loss ladder** (§29), **Business-invariant checks** (§30), **Plugin rent rubric** (§31), **Context ceilings** (§32), **Doc reference graph** (§33), **Anti-hallucination** (§34), **Past+Present+Future body** (§35), **Project trackers** (§36), **Doc ownership** (§37), **Archive-on-delete** (§38), **Sponsor + white-label** (§39 — moved to `playbooks/commercial-bound.md`), **Doc-vs-code drift** (§40), **Brand architecture** (§41), **Design system integration** (§42 — moved to `playbooks/tier-a-design.md`), **Session cognition** (§43), **Plugin dispatch** (§44), **Cross-repo clusters** (§45), **Tool-cascade workflow** (§46), **Multi-role agent matrix** (§47), **Parsimony / smallest-tool-first** (§48), **Audit triage discipline** (§49), **Source-of-truth matrix** (§50 — universal rows only; cluster-specific rows moved to playbooks), **Composite cascade catalog** (§51 — §51.2/51.4/51.6 moved to playbooks), **Session launch context + unattended-mode contract** (§52), **Recurrence detection + root-cause escalation** (§53). Sub-sections new in v44: **§4.5 cascade-commit exception**, **§17.b stale-P0 escalation**, **§32.5 canonical-doc size ceiling**, **§38.5 HANDOFF lifecycle enforcement**.

**Cluster playbooks** (per-repo `@-import` based on cluster membership): `~/.claude/conventions/playbooks/vps-infra.md` (DNS XOR for VPS-infra repos), `~/.claude/conventions/playbooks/deployed-service.md` (Sentry/Glitchtip XOR + production-incident triage + time-window correlation for repos with prod telemetry), `~/.claude/conventions/playbooks/tier-a-design.md` (Figma/Stitch + design system for Tier A/B), `~/.claude/conventions/playbooks/multi-lang.md` (cross-language refactor cascade for multi-language repos), `~/.claude/conventions/playbooks/commercial-bound.md` (sponsor-readiness + license-aware code-graph routing), `~/.claude/conventions/playbooks/brand-registry.md` (Vagary brand architecture for Vagary-family repos), `~/.claude/conventions/playbooks/bellring-cluster.md` (Bellring server↔extension; v1-stub), `~/.claude/conventions/playbooks/pulseboard-cluster.md` (Pulseboard Android↔Windows; v1-stub), `~/.claude/conventions/playbooks/vagary-cluster.md` (Vagary product cross-repo; v1-stub). **`tech-debt-audit.md`** is Read-on-demand (NOT @-imported) per ENTRY #169 §49 audit-triage discipline — invoked when user requests audit / tech-debt / dead-code work.

**Sources**: `~/.claude/conventions/universal-claudemd.md` (laws, MCP routing, lifecycle, rent rubric, doc-graph, anti-hallucination, brand architecture) + `~/.claude/conventions/project-hygiene.md` (doc placement, cleanup, archive-on-delete, ownership matrix) + cluster playbooks under `~/.claude/conventions/playbooks/` (loaded per-repo via `@-import` in `## Active Cluster Playbooks` section; see list above). Read relevant sections before significant work. Sync: `~/.claude/scripts/sync-preambles.py` (manual cadence; run after any source edit).

## Active Cluster Playbooks (per v40 cluster-split — content auto-inlined)
<!-- BEGIN PLAYBOOKS BLOCK (managed by sync-preambles.py — content inlined; source at ~/.claude/conventions/playbooks/) -->

Source @-imports (declarative pointer; content inlined below since Claude Code does not recursively expand `@-imports` in per-repo CLAUDE.md):
- `@~/.claude/conventions/playbooks/commercial-bound.md`
- `@~/.claude/conventions/playbooks/multi-lang.md`
- `@~/.claude/conventions/playbooks/brand-registry.md`

### Playbook: commercial-bound.md (verbatim from `~/.claude/conventions/playbooks/commercial-bound.md`)

# Commercial-bound + Sponsor-readiness Playbook

**VERSION: 2026-05-06-v1**
Loaded only in repos that are sponsor-ready public OSS, or commercial-bound (sold, embedded in paid product, or redistributed under permissive license). Per-repo `CLAUDE.md` `@-imports` this file when applicable.

Source: extracted verbatim from `~/.claude/conventions/universal-claudemd.md` v39 §39 + §50.2 during v40 cluster-split refactor. No content changes — only relocation so non-commercial / non-sponsor repos don't carry these rules.

**Applies to repos**: `aakhara`, `bellring-server`, `bellring-extension`, `bulk`, `pulseboard` (Android), `pulseboard-desktop`, `tldv_downloader`, `portfolio`, `project-template`, `vagary-platform` (sponsor-ready, has public-vertical surfaces), `host_page` (sponsor-ready landing template).

---

## 1. Sponsor-readiness + white-label pivot (originally §39)

### Sponsor-ready checklist for public repos
- `.github/FUNDING.yml` pointing to `github.com/sponsors/<user>`
- README "Sponsor" section near the top (badge + 1-paragraph ask)
- `LICENSE` (MIT for utilities, AGPL for commercial pressure, other for proprietary)
- At least one GitHub Release (binary attached if applicable, e.g. APK)
- CI green badge

### White-label pivot pattern
When an internal tool goes OSS (e.g. NetworkMonitorCN → **Pulseboard** rebrand 2026-04-19) OR an OSS utility forks into SaaS (e.g. **Bellring** — formerly codenamed Salvo — from sales-notification):

1. **Fork or publish** — new repo with clean name, no internal branding in code
2. **Strip tenant-specific** — remove hardcoded emails/domains/org IDs; parameterize via env/config
3. **Document "Fork + rebrand"** — README section listing the edits a downstream forker makes
4. **Record sibling spec** — `~/.claude/specs/YYYY-MM-DD-<name>-whitelabel.md` if a SaaS pivot
5. **Update inventory** — add to `repo-inventory.md` with sponsor-ready / white-label flags

### Current inventory (2026-04-19)
- **Sponsor-ready public**: tldv_downloader, bulk (renamed from `bulk_api_trigger` 2026-04-19), **pulseboard** (renamed from `NetworkMonitorCN` 2026-04-19), portfolio, project-template, vagary-platform (renamed from `index-of-news` 2026-04-19; flagship vertical retains Index of News brand)
- **White-label pivot applied**: **Bellring** (formerly codenamed Salvo) — repos `bellring-server` + `bellring-extension` (renamed from `sales-notification-backend` / `sales-notification-extension` 2026-04-19). Spec: `~/.claude/specs/2026-04-19-sales-notification-whitelabel.md`.
- **Recently renamed (2026-04-19 Phase 3)**: `sales-notification-backend` → `bellring-server`, `sales-notification-extension` → `bellring-extension`, `NetworkMonitorCN` → `pulseboard`, `training-bot` → `aakhara`.
- **Recently renamed (2026-04-19 Phases 1-2)**: `AI_voice_builder` → `vagary-voice`, `chat-bot` → `anjaan-app`, `bulk_api_trigger` → `bulk`, `index-of-news` → `vagary-platform`. `webhook_trigger` archived (superseded by `bulk`). See `~/.claude/conventions/project-hygiene.md` § Rename Propagation Protocol.
- **Brand umbrella**: Vagary Labs (tech/R&D division of Vagary Life Pvt Ltd; see §41) holds the platform + products + OSS utilities.

## 2. License-aware tool routing (originally §50.2)

Repos categorized as **commercial-bound** (will be sold, embedded in paid product, or redistributed under permissive license):
- `bellring-server`, `bellring-extension` (Bellring SaaS — paid tiers)
- `aakhara` (paid sales-training product)
- `pulseboard`, `pulseboard-desktop` (Public OSS; permissive license required for derivatives)

When working in commercial-bound repos:
- `gitnexus` MCP MAY be used for **read-only investigation** (cypher queries, impact analysis in conversation)
- `gitnexus wiki`, `gitnexus group sync` derivatives, indexed JSON exports MUST NOT be committed/shipped (PolyForm-NC contamination)
- `codegraphcontext` MCP is the canonical graph-derivative source for these repos

When working in **personal/private repos** (vagary-platform, vagary-voice, vagary-earnings, ASM, anjaan-app, internal Cramraika): GitNexus permitted freely.

Per-repo CLAUDE.md should declare classification: `## License classification: commercial-bound` or `## License classification: personal/private`.

### Playbook: multi-lang.md (verbatim from `~/.claude/conventions/playbooks/multi-lang.md`)

# Multi-Language Refactor Playbook

**VERSION: 2026-05-06-v1**
Loaded only in repos that span ≥2 language extensions (.py + .ts + .kt + .go etc.). Per-repo `CLAUDE.md` `@-imports` this file when applicable.

Source: extracted verbatim from `~/.claude/conventions/universal-claudemd.md` v39 §51.4 during v40 cluster-split refactor. No content changes — only relocation so single-language repos don't carry the cross-language refactor cascade.

**Applies to repos**: `vagary-platform` (Python + TypeScript + React), `vagary-voice` (Python + TypeScript + Kotlin + Go), `Automated-sales-manager-main` (TypeScript + HTML/HTMX), `aakhara` (Python + TypeScript), `anjaan-app` (Python + JS), `bellring-server` + `bellring-extension` (when treating as a coupled cluster).

---

## §51.4 Cross-language refactor (originally §51.4 of universal)

**Trigger**: user says "rename across", "refactor X across the platform", or paths span ≥2 language extensions (.py + .ts + .kt).
**Sequence**:
1. `mcp__gitnexus__rename dry_run=true` — preview text-search hits across languages
2. Review "graph"-tagged hits (LSP-like confidence) vs "text_search"-tagged (manual review)
3. Per language, apply: `ast-grep --rewrite '<pattern>' '<replacement>'` for batch shape changes
4. Per language, run Serena `rename_symbol` for LSP-validated single-language rename
5. `/graph-audit` A8 (METHOD_OVERRIDES drift) — verify override chains intact
6. `semgrep --baseline` — regression check
7. Phase D verify per §46

Cross-language is the gap §47 Developer mode doesn't differentiate; this cascade explicitly serves it.

### Playbook: brand-registry.md (verbatim from `~/.claude/conventions/playbooks/brand-registry.md`)

# Brand Registry Playbook

**VERSION: 2026-05-07-v1**
Loaded only in Vagary-family repos (per `~/.claude/conventions/repo-inventory.md` §45). Per-repo `CLAUDE.md` `@-imports` this file when applicable.

Source: extracted verbatim from `~/.claude/conventions/universal-claudemd.md` §41 (Brand architecture) during 2026-05-07 cluster-split refinement (ENTRY #168). No content changes — only relocation so non-Vagary repos (e.g. `metabase-cn`, `tldv_downloader`, `torn-smart-scripts`) don't load 64 lines of Vagary brand registry they have no use for.

**Applies to repos**: `vagary-platform`, `vagary-voice`, `anjaan-app`, `aakhara`, `bellring-server`, `bellring-extension`, `bulk`, `pulseboard`, `pulseboard-desktop`, `project-template`, `portfolio` (cross-link only), `host_page`, `vps_host`, `vps-ansible`, `platform-docs`, `vagary-earnings`.

---

## 41. Brand architecture (originally §41 of universal-claudemd.md)

Vagary Life Pvt Ltd is the **corporate parent**. Below it, product and tech activity is organized into named divisions. As of 2026-04-19, one division is formalized: **Vagary Labs** (tech/R&D/platform).

### Structure

```
Vagary Life Pvt Ltd (parent company; registered entity)
└── Vagary Labs (tech/R&D/platform division — vagarylabs.com [PENDING])
    ├── Platform
    │   └── vagary-platform (20-vertical substrate; repo renamed from `index-of-news` 2026-04-19)
    │       └── Index of News (flagship vertical; keeps its own news sub-brand + 6 domains)
    ├── Product brands (each lives as an independent product under its own domain)
    │   ├── Vagary Voice (vagaryvoice.cloud) — commercial voice-AI SaaS
    │   ├── Anjaan (anjaan.online) — Hinglish consumer chat
    │   ├── Bellring (.io/.app/.ai TBD) — whitelabel sale-celebration SaaS; repos `bellring-server` + `bellring-extension` (renamed from `sales-notification-*` 2026-04-19; formerly codenamed Salvo)
    │   ├── Aakhara (aakhara.com pending) — voice sales-training roleplay for BDEs (Sanskrit "आखाड़ा" = practice arena; repo renamed from `training-bot` 2026-04-19). Positioning TBD: could sit as Vagary Voice sub-product or stand alone
    │   └── Hype / Mockline / Kohort (legacy proposed names, superseded by Bellring/Aakhara above)
    └── OSS Utilities
        ├── bulk (renamed from `bulk_api_trigger` 2026-04-19)
        ├── tldv_downloader
        ├── pulseboard (renamed from `NetworkMonitorCN` 2026-04-19; Android OSS, `pulseboard.build` pending)
        └── project-template
```

Additional divisions (media, ops, consulting, etc.) may be added later. Keep Vagary Labs scoped to **tech/platform/R&D**.

### Domain strategy

- **vagarylife.com / vagarylife.in** — corporate parent marketing + investor/careers. TO BE BUILT.
- **vagarylabs.com** — tech/R&D division site. Domain **PENDING PURCHASE** (user flagged). Will host platform docs + OSS index + R&D blog once acquired.
- **Per-product domains** — each commercial product keeps its own brand domain (`vagaryvoice.cloud`, `anjaan.online`, future `hype.sh`, etc.). Product domains do NOT nest under `vagarylabs.com`.
- **chinmayramraika.in** — founder's personal hub; cross-links each Vagary Life / Vagary Labs product in a "projects" section.

### Repo-to-brand mapping (authoritative)

| Repo | Vagary Labs home | Product / sub-brand |
|---|---|---|
| `vagary-platform` | Platform | Holds all 20 verticals; flagship vertical = **Index of News** (news sub-brand, 6 domains) |
| `vagary-voice` | Product brands | **Vagary Voice** (commercial product, `vagaryvoice.cloud`) |
| `anjaan-app` | Product brands | **Anjaan** (consumer product, `anjaan.online`) |
| `aakhara` | Product brands | **Aakhara** (voice sales-training roleplay; `aakhara.com` pending). Renamed from `training-bot` 2026-04-19. Positioning TBD (standalone OR Vagary Voice sub-product) |
| `bellring-server` | Product brands | **Bellring** server (whitelabel sale-celebration SaaS backend; `.io/.app/.ai` TBD). Renamed from `sales-notification-backend` 2026-04-19 (formerly codenamed Salvo) |
| `bellring-extension` | Product brands | **Bellring** extension (Chrome MV3 + Firefox/Edge portable; pairs with `bellring-server`). Renamed from `sales-notification-extension` 2026-04-19 |
| `bulk`, `tldv_downloader`, `pulseboard`, `project-template` | OSS Utilities | Each with its own GitHub + README brand. `pulseboard` renamed from `NetworkMonitorCN` 2026-04-19 (Android OSS; `pulseboard.build` pending) |
| `portfolio` | Personal hub (OUTSIDE Vagary Labs) | `chinmayramraika.in` founder site |
| `host_page`, `platform-docs`, `vps_host`, `n8n-workflows`, `metabase-cn` | Infrastructure (internal to Vagary Labs) | No external product brand |
| `Automated-sales-manager-main` | Client work (CN-internal) | ASM — CN-branded; Cadre whitelabel TBD |
| `google-sheet-sales-manager` | Client work (CN-internal) | Sheetpilot whitelabel TBD |
| `Expense tracker` | Absorbing → Platform (`budget` vertical) | No standalone brand going forward |

### How Claude uses this

- When a repo's description says "product," check the brand table above for positioning.
- The **platform repo** (`vagary-platform`) is *not* a product. It is substrate. Individual verticals (news, budget, …) are the products that ship.
- Don't reinvent brand positioning in per-repo CLAUDE.md — reference this section and defer details to `~/.claude/specs/2026-04-19-brand-rename-proposal.md` (for rationale) + `~/.claude/conventions/repo-inventory.md` (for current state).
- For any new repo: declare its division home in its CLAUDE.md § Status / Brand section and cross-reference here.

### Caveats

- `vagarylabs.com` is **not yet purchased** (2026-04-19). Until acquired, Vagary Labs is an internal organizational concept; do not publish external references to `vagarylabs.com` until DNS is live.
- Additional divisions (media, ops, consulting) may emerge. When they do, add a sibling subtree here + bump VERSION.

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
