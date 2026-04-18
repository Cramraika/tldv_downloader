# TLDV Downloader

## Claude Preamble
<!-- VERSION: 2026-04-19-v8 -->
<!-- SYNC-SOURCE: ~/.claude/conventions/universal-claudemd.md -->

**Universal laws** (§4), **MCP routing** (§6), **Drift protocol** (§11), **Dynamic maintenance** (§14), **Capability resolution** (§15), **Subagent SKILL POLICY** (§16), **Session continuity** (§17), **Decision queue** (§17.a), **Attestation** (§18), **Cite format** (§19), **Three-way disagreement** (§20), **Pre-conditions** (§21), **Provenance markers** (§22), **Redaction rules** (§23), **Token budget** (§24), **Tool-failure fallback** (§25), **Prompt-injection rule** (§26), **Append-only discipline** (§27), **BLOCKED_BY markers** (§28), **Stop-loss ladder** (§29), **Business-invariant checks** (§30), **Plugin rent rubric** (§31), **Context ceilings** (§32).

**Sources**: `~/.claude/conventions/universal-claudemd.md` (laws, MCP routing, lifecycle, rent rubric) + `~/.claude/conventions/project-hygiene.md` (doc placement, cleanup, local-workspaces). Read relevant sections before significant work. Re-audit due **2026-07-19**. Sync: `~/.claude/scripts/sync-preambles.py`.

## Products

| Product | What It Does | Who Uses It | Status |
|---------|-------------|-------------|--------|
| Single Meeting Downloader | Downloads one TLDV meeting recording by URL using HLS stream capture | Developer (Chinmay) | Inactive |
| Batch Downloader | Parallel downloads of multiple meeting recordings from a list of URLs | Developer (Chinmay) | Inactive |

## Product Details

### Single Meeting Downloader
- **User journey**: Get auth token from tldv.io browser session (Network tab) -> Run script with meeting URL -> Script fetches meeting metadata from TLDV API -> Extracts HLS stream URL -> Downloads via N_m3u8DL-RE or FFmpeg -> Saves as MP4 with sanitized filename
- **Success signals**: Meeting video saved locally within minutes; filename includes meeting title and date
- **Failure signals**: Auth token expired (401); HLS stream URL changed format; download tool not on PATH

### Batch Downloader
- **User journey**: Prepare list of meeting URLs -> Run in batch mode -> Downloads execute in parallel (ThreadPoolExecutor) -> Progress shown per download -> All files saved to local directory
- **Success signals**: All meetings downloaded without manual babysitting; no partial/corrupt files
- **Failure signals**: Some downloads fail silently; parallel downloads overwhelm network; duplicate downloads

## Tech Reference

### Stack
- **Runtime**: Python 3.7+ (single script: `tldv_downloader.py`)
- **HTTP**: requests library
- **Download tools**: N_m3u8DL-RE (preferred) or FFmpeg for HLS stream downloading
- **Parallelism**: concurrent.futures.ThreadPoolExecutor
- **Tier**: C (Stable/Maintenance) -- not actively used

### File Organization
- Never save working files to root folder
- `tldv_downloader.py` - Main script (single-file architecture)
- `requirements.txt` - Python dependency (requests)

### Build & Test
```bash
# Install
pip install -r requirements.txt

# Run
python tldv_downloader.py              # Interactive mode
python tldv_downloader.py --help       # Show auth token help
```

### Prerequisites
- N_m3u8DL-RE (recommended) or FFmpeg must be installed and on PATH
- Auth token obtained from tldv.io browser session (Network tab)

### n8n Workflow Automation

This project can trigger and receive n8n workflows at `https://n8n.chinmayramraika.in`.

- **Webhook URL:** Set in `N8N_WEBHOOK_URL` env var
- **API Key:** Set in `N8N_API_KEY` env var (unique per project)
- **Auth Header:** `X-API-Key: <N8N_API_KEY>`
- **Workflow repo:** github.com/Cramraika/n8n-workflows (private)

## VPS Services Integration

This repo is **not deployed on VPS** (runs locally). When VPS deployment is needed, the following services are available:

### Available Observability Stack
- **GlitchTip** (errors.chinmayramraika.in): Create a project to capture errors
- **Loki + Grafana** (grafana.chinmayramraika.in): Container log aggregation via Promtail Docker SD
- **Uptime Kuma** (status.chinmayramraika.in): Add a monitor for uptime tracking
- **Netdata** (monitor.chinmayramraika.in): System metrics + custom alarms

### Available Notifications
- **Slack**: Deploys → #deploys, Errors → #errors, CI → #ci, Kuma alerts → #cron
- **Telegram**: Critical alerts → @vpsmgr_bot (chat 710228663)
- **Email**: Netdata + Uptime Kuma → chinu.ramraika@gmail.com

### Available Secrets Management
- **Infisical** (secrets.chinmayramraika.in): Create a workspace when deploying to VPS
- Delivery: Infisical Agent on VPS renders env file → docker-compose env_file mount

### Security Rules
- NEVER hardcode API keys, secrets, or credentials in any file
- NEVER pass credentials as inline env vars in Bash commands
- NEVER commit .env, .claude/settings.local.json, or .mcp.json to git
- Always validate user input at system boundaries
