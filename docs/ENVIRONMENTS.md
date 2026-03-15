# Environments - TLDV Downloader

**Repo**: Cramraika/tldv_downloader
**Stack**: Python 3.7+ (single script) + requests

---

## Local Development

### Prerequisites

- Python 3.7+
- pip
- **N_m3u8DL-RE** (recommended) or **FFmpeg** -- at least one must be installed and on PATH
- A tldv.io account with access to the meetings you want to download

### Installation

```bash
git clone https://github.com/Cramraika/tldv_downloader.git
cd tldv_downloader

# Install Python dependency
pip install -r requirements.txt
```

### Dependencies

- `requests==2.32.5` -- HTTP client (the only Python dependency)

### Installing Download Tools

**N_m3u8DL-RE** (recommended -- significantly faster):
```bash
# macOS
brew install n_m3u8dl-re

# Windows (scoop)
scoop install n_m3u8dl-re

# Manual: https://github.com/nilaoda/N_m3u8DL-RE/releases
```

**FFmpeg** (fallback):
```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Windows (chocolatey)
choco install ffmpeg
```

Verify installation:
```bash
N_m3u8DL-RE --version   # or
ffmpeg -version
```

### Usage

```bash
# Interactive mode (single or batch download)
python tldv_downloader.py

# Show help for getting the auth token
python tldv_downloader.py --help
```

The script runs interactively and prompts for:
1. Single or batch download mode
2. tldv.io meeting URL(s)
3. Authorization token (from browser)
4. Output directory (optional)
5. Number of parallel workers (batch mode, 1-8, default 3)

### Getting the Authorization Token

1. Go to https://tldv.io/ and log in
2. Open Developer Tools (F12)
3. Go to the **Network** tab
4. Refresh the page (F5)
5. Filter by `watch-page`
6. Click the request to `...meetings/.../watch-page?noTranscript=true`
7. Copy the `Authorization` header value (starts with `Bearer `)

Notes:
- One token works for multiple downloads in the same session
- Token expires when you log out or close the browser
- Get a fresh token if downloads start failing

### Batch Download from File

Create a text file with one URL per line:
```text
# Comments start with #
https://tldv.io/app/meetings/abc123
https://tldv.io/app/meetings/def456
```

Then choose option 2 (file input) when prompted in batch mode.

### Output Structure

```
output_directory/
  2025-05-08_14-30-29_Meeting_Name.mp4    # Video file
  2025-05-08_14-30-29_Meeting_Name.json   # Meeting metadata
```

---

## Environment Variables

**None required.** Authentication is handled via the interactive auth token prompt at runtime.

---

## Production / Deployment

**Current status**: CLI tool only. No server or deployment pipeline.

This is a local utility script -- not deployed anywhere. Run it on your machine when you need to download tldv.io recordings.

---

## CI/CD

**Pipeline**: GitHub Actions on `ubuntu-latest` (Python 3.11)
**Triggers**: Push/PR to `main` or `master`

| Step | Description |
|------|-------------|
| Lint (flake8) | Checks for syntax errors and undefined names |
| Import Verify | Validates `requests` can be imported |
| Security Audit | `pip-audit` (continue on error) |

---

## Troubleshooting

**"Neither N_m3u8DL-RE nor ffmpeg is available"**
- Install at least one downloader (see Installation above)
- Ensure it is on your system PATH
- Test: `N_m3u8DL-RE --version` or `ffmpeg -version`

**"Unauthorized: Invalid auth token"**
- Get a fresh token from the browser (see Getting the Authorization Token)
- Ensure you are logged into tldv.io
- Copy the complete `Authorization` header value including `Bearer `

**"Meeting not found"**
- Verify the URL is correct
- Ensure you have access to the meeting on tldv.io
- Try refreshing the tldv.io page first

**Downloads fail after working initially**
- Token has expired -- get a fresh one
- Check your internet connection
- Ensure disk space is available (videos can be large)

**Slow downloads**
- Use N_m3u8DL-RE instead of FFmpeg for parallel segment downloading
- In batch mode, start with 3 workers and adjust based on network speed
