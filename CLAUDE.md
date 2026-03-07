# TLDV Downloader

## Project Overview
- **Stack**: Python 3.7+ (single script) + requests library
- **Description**: CLI tool to download videos from tldv.io with support for single and parallel batch downloads. Uses N_m3u8DL-RE or FFmpeg for HLS stream downloading, with session-based auth token management.
- **Tier**: C (Stable/Maintenance)

## File Organization
- Never save working files to root folder
- `tldv_downloader.py` - Main script (single-file architecture)
- `requirements.txt` - Python dependency (requests)

## Build & Test
```bash
# Install
pip install -r requirements.txt

# Run
python tldv_downloader.py              # Interactive mode
python tldv_downloader.py --help       # Show auth token help
```

## Prerequisites
- N_m3u8DL-RE (recommended) or FFmpeg must be installed and on PATH
- Auth token obtained from tldv.io browser session (Network tab)

## Security Rules
- NEVER hardcode API keys, secrets, or credentials in any file
- NEVER pass credentials as inline env vars in Bash commands
- NEVER commit .env, .claude/settings.local.json, or .mcp.json to git
- Always validate user input at system boundaries
