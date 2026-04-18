# 🎬 TLDV Video Downloader

> **Export your tldv.io meeting recordings to local MP4 — single or bulk, parallel, resumable.**

[![GitHub Sponsors](https://img.shields.io/github/sponsors/Cramraika?logo=github&label=Sponsor)](https://github.com/sponsors/Cramraika)
[![Stars](https://img.shields.io/github/stars/Cramraika/tldv_downloader?style=social)](https://github.com/Cramraika/tldv_downloader/stargazers)
[![License](https://img.shields.io/github/license/Cramraika/tldv_downloader)](./LICENSE)
[![Issues](https://img.shields.io/github/issues/Cramraika/tldv_downloader)](https://github.com/Cramraika/tldv_downloader/issues)

Download videos from tldv.io at your own pace — keep your recordings for offline watch, archives, or compliance. Single downloads or parallel batch, with smart resume and metadata preservation. Works on Windows, macOS, and Linux.

## Who is this for?

- **Sales teams** archiving customer conversations for review
- **Researchers** collecting interview recordings
- **Solo operators** keeping a local library of their meetings
- **Anyone** who doesn't want their recordings locked behind a SaaS subscription

## 💖 Sponsor

If this saves you time, [sponsor on GitHub](https://github.com/sponsors/Cramraika) — your support funds ongoing maintenance and new features (UI wrapper, Whisper transcription, Obsidian export). Or [reach out](https://chinmayramraika.in) about enterprise/custom work.

## ✨ Features

- **Fast Downloads**: Prioritizes N_m3u8DL-RE for parallel segment downloading
- **Batch Processing**: Download multiple videos simultaneously with configurable workers
- **Smart Fallback**: Uses FFmpeg if N_m3u8DL-RE is not available
- **Filename Sanitization**: Automatically handles invalid characters and long names
- **Session Management**: One auth token works for multiple downloads
- **Metadata Preservation**: Saves meeting information as JSON files
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Progress Tracking**: Real-time download progress and file size reporting

## 🚀 Quick Start

### Prerequisites

1. **Python 3.7+**
2. **N_m3u8DL-RE** (recommended) or **FFmpeg**
3. **requests** library

### Installation

1. **Install Python dependencies:**
   ```bash
   pip install requests
   ```

2. **Install N_m3u8DL-RE (recommended for faster downloads):**
   - Download from: https://github.com/nilaoda/N_m3u8DL-RE/releases
   - Extract and add to your system PATH
   - Or use package manager:
     ```bash
     # Windows (using scoop)
     scoop install n_m3u8dl-re
     
     # macOS (using homebrew)
     brew install n_m3u8dl-re
     ```

3. **Install FFmpeg (backup option):**
   ```bash
   # macOS
   brew install ffmpeg
   
   # Windows (using chocolatey)
   choco install ffmpeg
   
   # Linux (Ubuntu/Debian)
   sudo apt update && sudo apt install ffmpeg
   ```

### Usage

1. **Run the script:**
   ```bash
   python tldv_downloader.py
   ```

2. **Get help for auth token:**
   ```bash
   python tldv_downloader.py --help
   ```

## 🔐 Getting Authorization Token

The auth token is tied to your login session and can be reused for multiple downloads:

### Step-by-Step Guide:

1. **Login to TLDV:**
   - Go to https://tldv.io/ and login

2. **Open Developer Tools:**
   - Press F12 or right-click → "Inspect"

3. **Find the Network Request:**
   - Go to "Network" tab
   - Refresh the page (F5)
   - In the filter box, type: `watch-page`
   - Look for: `...meetings/.../watch-page?noTranscript=true`

4. **Copy Authorization Token:**
   - Click on the request → "Headers" → "Request Headers"
   - Copy the entire "Authorization" value (starts with "Bearer ")

### Important Notes:
- ✅ One token works for multiple videos in the same session
- ⏰ Token expires when you log out or close browser
- 🔄 Get a fresh token if downloads start failing
- 💡 Keep browser tab open while downloading

## 📖 Usage Examples

### Single Video Download

```bash
python tldv_downloader.py
```

Follow the prompts:
- Enter TLDV meeting URL
- Enter authorization token  
- Choose output directory (optional)
- Confirm download

### Batch Download (Multiple Videos)

```bash
python tldv_downloader.py
```

Choose batch mode when prompted:
- Select input method (manual entry or file)
- Enter URLs or provide text file
- Enter authorization token (same for all)
- Set number of parallel workers (1-8)
- Confirm batch download

### URLs Text File Format

Create a text file with one URL per line:

```text
# My TLDV Downloads
https://tldv.io/app/meetings/681cc00576bb060013e5fbb7
https://tldv.io/app/meetings/582ab11487cc070012d5fa6c
https://tldv.io/app/meetings/793de22598dd080013f6gb8d

# Comments start with #
# Empty lines are ignored
```

## ⚙️ Configuration Options

### Parallel Downloads
- **Workers**: 1-8 (default: 3)
- **Recommendation**: 
  - 3-4 workers for most systems
  - 2 workers for slower connections
  - 6-8 workers for high-speed connections

### Output Structure
```
output_directory/
├── 2025-05-08_14-30-29_Meeting_Name.mp4
├── 2025-05-08_14-30-29_Meeting_Name.json
├── 2025-05-08_15-45-12_Another_Meeting.mp4
└── 2025-05-08_15-45-12_Another_Meeting.json
```

## 🔧 Troubleshooting

### Common Issues

**1. "Neither N_m3u8DL-RE nor ffmpeg is available"**
- Install at least one downloader (see Installation section)
- Ensure it's added to your system PATH
- Test with `N_m3u8DL-RE --version` or `ffmpeg -version`

**2. "Unauthorized: Invalid auth token"**
- Get a fresh token from browser
- Ensure you're logged into tldv.io
- Copy the complete "Authorization" header value

**3. "Meeting not found"**
- Check if URL is correct
- Ensure you have access to the meeting
- Try refreshing the browser page first

**4. Downloads fail after working initially**
- Token has expired - get a fresh one
- Check your internet connection
- Verify meeting is still accessible

### Performance Tips

- **Use N_m3u8DL-RE** for significantly faster downloads
- **Parallel workers**: Start with 3, adjust based on performance
- **Network**: Stable connection recommended for batch downloads
- **Storage**: Ensure sufficient disk space (videos can be large)

## 🎯 Advanced Features

### Filename Sanitization
- Removes invalid characters: `<>:"/\|?*`
- Handles long filenames (truncates to 100 chars)
- Preserves readable format: `YYYY-MM-DD_HH-MM-SS_Meeting_Name.mp4`

### Metadata Preservation
Each download creates a JSON file with:
- Meeting information
- Participant details
- Recording timestamps
- Original API response

### Error Recovery
- Automatic retry on network failures
- Graceful handling of invalid URLs
- Detailed error reporting
- Partial download recovery

## 📊 Performance Comparison

| Downloader | Speed | Features | Compatibility |
|-----------|-------|----------|---------------|
| **N_m3u8DL-RE** | ⭐⭐⭐⭐⭐ | Parallel segments, advanced options | Modern |
| **FFmpeg** | ⭐⭐⭐ | Reliable, universal support | Universal |

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests!

## 📄 License

This project is for educational purposes. Respect tldv.io's terms of service.

## ⚠️ Disclaimer

- Use responsibly and in accordance with tldv.io's terms of service
- Ensure you have permission to download the content
- This tool is for personal use and backup purposes
- Large-scale automated downloading may violate terms of service

---

**Made with ❤️ for the community**

*Last updated: August 2025*