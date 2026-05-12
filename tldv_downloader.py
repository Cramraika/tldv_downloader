#!/usr/bin/env python3
"""
TLDV Video Downloader with N_m3u8DL-RE Support
Enhanced version with better error handling, filename sanitization, and N_m3u8DL-RE integration
"""

import re
import json
import tempfile
import requests
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

GAIA_BASE = "https://gaia.tldv.io"
GW_BASE = "https://gw.tldv.io"


class TLDVDownloader:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def sanitize_filename(self, name):
        """Remove invalid characters from filename"""
        # Remove invalid characters and replace with underscores
        sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
        # Remove multiple consecutive underscores
        sanitized = re.sub(r'_{2,}', '_', sanitized)
        # Remove leading/trailing underscores and spaces
        sanitized = sanitized.strip('_ ')
        # Limit length to avoid filesystem issues
        if len(sanitized) > 100:
            sanitized = sanitized[:100]
        return sanitized or "TLDV_Meeting"

    def extract_meeting_id(self, url):
        """Extract meeting ID from TLDV URL"""
        url = url.strip().rstrip('/')
        try:
            meeting_id = url.split('/')[-1]
            # Basic validation for meeting ID format
            if len(meeting_id) < 10:
                raise ValueError("Invalid meeting ID format")
            return meeting_id
        except (IndexError, ValueError) as e:
            raise ValueError(f"Could not extract meeting ID from URL: {url}") from e

    def prepare_auth_token(self, token):
        """Ensure auth token has Bearer prefix if needed"""
        token = token.strip()
        if not token.startswith('Bearer ') and not token.startswith('bearer '):
            token = f"Bearer {token}"
        return token

    def fetch_meeting_data(self, meeting_id, auth_token):
        """Fetch meeting data from TLDV API"""
        api_url = f"{GW_BASE}/v1/meetings/{meeting_id}/watch-page?noTranscript=true"

        headers = {
            "Authorization": auth_token,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        try:
            response = self.session.get(api_url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise ValueError("Unauthorized: Invalid auth token") from e
            elif response.status_code == 404:
                raise ValueError("Meeting not found") from e
            else:
                raise ValueError(f"API error: {e}") from e
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error: {e}") from e

    @staticmethod
    def _caesar_shift(text, shift):
        """Apply caesar shift on letters; digits/punctuation untouched."""
        out = []
        for ch in text:
            if 'a' <= ch <= 'z':
                out.append(chr((ord(ch) - ord('a') + shift) % 26 + ord('a')))
            elif 'A' <= ch <= 'Z':
                out.append(chr((ord(ch) - ord('A') + shift) % 26 + ord('A')))
            else:
                out.append(ch)
        return ''.join(out)

    def fetch_decoded_playlist(self, meeting_id, auth_token):
        """Fetch the signed HLS playlist from gaia and decode obfuscated segment URLs.

        Flow:
          GET gaia.tldv.io/v1/meetings/{id}/playlist.m3u8 -> 302 puttanesca proxy ->
          media playlist with #TLDVCONF:<expires>,<shift>,<prefix> header and
          caesar-shifted segment filenames. Decode back to absolute signed S3 URLs.
        """
        api_url = f"{GAIA_BASE}/v1/meetings/{meeting_id}/playlist.m3u8"
        headers = {"Authorization": auth_token, "Accept": "application/vnd.apple.mpegurl"}
        try:
            response = self.session.get(api_url, headers=headers, timeout=30, allow_redirects=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            code = getattr(e.response, "status_code", None)
            if code == 401:
                raise ValueError("Unauthorized: Invalid auth token") from e
            if code == 403:
                raise ValueError("Forbidden: insufficient permission for this meeting") from e
            if code == 404:
                raise ValueError("Meeting playlist not found") from e
            raise ValueError(f"Playlist API error: {e}") from e
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Network error fetching playlist: {e}") from e

        raw = response.text
        prefix = ""
        shift = 0
        out_lines = ["#EXTM3U"]
        for line in raw.splitlines():
            if line.startswith("#TLDVCONF:"):
                parts = line[len("#TLDVCONF:"):].split(",", 2)
                if len(parts) >= 3:
                    try:
                        shift = int(parts[1])
                    except ValueError:
                        shift = 0
                    prefix = parts[2]
                continue
            if line.startswith("#EXTM3U"):
                continue
            if line.startswith("#") or not line.strip():
                out_lines.append(line)
            else:
                out_lines.append(prefix + self._caesar_shift(line, shift))

        if not prefix:
            raise ValueError("Playlist did not contain #TLDVCONF header; format may have changed")
        return "\n".join(out_lines) + "\n"

    def parse_meeting_info(self, data):
        """Parse meeting information from API response"""
        meeting = data.get("meeting", {})
        video = data.get("video", {})

        name = meeting.get("name", "TLDV_Meeting")
        created_at = meeting.get("createdAt")
        source_url = video.get("source")  # informational only; unsigned, not used for download

        # Parse date
        try:
            if created_at:
                date_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                date_obj = datetime.now()
        except ValueError:
            date_obj = datetime.now()

        timestamp = date_obj.strftime("%Y-%m-%d_%H-%M-%S")
        sanitized_name = self.sanitize_filename(name)

        return {
            'name': sanitized_name,
            'timestamp': timestamp,
            'source_url': source_url,
            'full_data': data
        }

    def check_downloader_availability(self):
        """Check if N_m3u8DL-RE or ffmpeg is available"""
        downloaders = [
            {'name': 'N_m3u8DL-RE', 'cmd': 'N_m3u8DL-RE', 'version_cmd': '--version', 'preferred': True},
            {'name': 'ffmpeg', 'cmd': 'ffmpeg', 'version_cmd': '--version', 'preferred': False},
            {'name': 'ffmpeg', 'cmd': 'ffmpeg', 'version_cmd': '-version', 'preferred': False},
        ]

        available = []
        for downloader in downloaders:
            try:
                result = subprocess.run(
                    [downloader['cmd'], downloader['version_cmd']],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                if result.returncode == 0:
                    available.append(downloader)
                    print(f"✅ {downloader['name']} is available")
                else:
                    print(f"❌ {downloader['name']} not working properly")
            except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
                print(f"❌ {downloader['name']} not found")

        if not available:
            raise RuntimeError("Neither N_m3u8DL-RE nor ffmpeg is available. Please install one of them.")

        # Return preferred downloader (N_m3u8DL-RE if available)
        preferred = next((d for d in available if d['preferred']), available[0])
        return preferred

    def download_with_n_m3u8dl_re(self, playlist_path, output_file):
        """Download using N_m3u8DL-RE from a local decoded playlist file."""
        command = [
            'N_m3u8DL-RE',
            str(playlist_path),
            '--save-name', Path(output_file).stem,
            '--save-dir', str(Path(output_file).parent),
            '--thread-count', '8',
            '--download-retry-count', '3',
            '--auto-select',
            '--no-log',
        ]
        return self._run_download_command(command, output_file)

    def download_with_ffmpeg(self, playlist_path, output_file):
        """Download using ffmpeg from a local decoded playlist file."""
        command = [
            'ffmpeg',
            '-protocol_whitelist', 'file,http,https,tcp,tls',
            '-allowed_extensions', 'ALL',
            '-i', str(playlist_path),
            '-c', 'copy',
            '-bsf:a', 'aac_adtstoasc',
            '-y',
            str(output_file),
        ]
        return self._run_download_command(command, output_file)

    def _run_download_command(self, command, output_file):
        """Run download command with progress tracking"""
        try:
            print(f"🚀 Starting download...")
            print(f"📁 Output: {output_file}")

            # Run the command
            result = subprocess.run(
                command,
                capture_output=False,  # Show live output
                text=True,
                timeout=3600  # 1 hour timeout
            )

            if result.returncode == 0:
                if Path(output_file).exists():
                    file_size = Path(output_file).stat().st_size
                    print(f"✅ Download completed successfully!")
                    print(f"📊 File size: {file_size / (1024 * 1024):.2f} MB")
                    return True
                else:
                    print("❌ Download command succeeded but file not found")
                    return False
            else:
                print(f"❌ Download failed with return code: {result.returncode}")
                return False

        except subprocess.TimeoutExpired:
            print("❌ Download timed out after 1 hour")
            return False
        except Exception as e:
            print(f"❌ Download error: {e}")
            return False

    def save_metadata(self, data, filename):
        """Save meeting metadata as JSON"""
        json_file = f"{filename}.json"
        try:
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Metadata saved: {json_file}")
        except Exception as e:
            print(f"⚠️ Could not save metadata: {e}")

    def download_multiple_videos(self, video_data_list, output_dir=None, max_workers=3):
        """Download multiple videos in parallel"""
        if not video_data_list:
            print("❌ No videos to download")
            return []

        # Setup output directory
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        else:
            output_path = Path.cwd()

        print(f"🚀 Starting parallel download of {len(video_data_list)} videos")
        print(f"🔧 Using {max_workers} parallel workers")
        print(f"📁 Output directory: {output_path}")

        successful_downloads = []
        failed_downloads = []

        def download_single(video_data):
            """Download a single video - thread-safe wrapper"""
            url, auth_token = video_data
            try:
                # Create a new session for each thread
                thread_downloader = TLDVDownloader()
                result = thread_downloader.download_video(url, auth_token, output_path)
                if result:
                    return {'success': True, 'url': url, 'file': result}
                else:
                    return {'success': False, 'url': url, 'error': 'Download failed'}
            except Exception as e:
                return {'success': False, 'url': url, 'error': str(e)}

        # Execute parallel downloads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all download tasks
            future_to_url = {
                executor.submit(download_single, video_data): video_data[0]
                for video_data in video_data_list
            }

            # Process completed downloads
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    if result['success']:
                        successful_downloads.append(result)
                        print(f"✅ Completed: {url}")
                    else:
                        failed_downloads.append(result)
                        print(f"❌ Failed: {url} - {result.get('error', 'Unknown error')}")
                except Exception as e:
                    failed_downloads.append({'success': False, 'url': url, 'error': str(e)})
                    print(f"💥 Exception for {url}: {e}")

        # Summary
        print(f"\n📊 Download Summary:")
        print(f"✅ Successful: {len(successful_downloads)}")
        print(f"❌ Failed: {len(failed_downloads)}")

        if successful_downloads:
            print(f"\n🎉 Downloaded files:")
            for download in successful_downloads:
                print(f"   📁 {download['file']}")

        if failed_downloads:
            print(f"\n💥 Failed downloads:")
            for download in failed_downloads:
                print(f"   ❌ {download['url']}: {download['error']}")

    def download_video(self, url, auth_token, output_dir=None):
        """Main download function"""
        try:
            # Setup output directory
            if output_dir:
                output_path = Path(output_dir)
                output_path.mkdir(parents=True, exist_ok=True)
            else:
                output_path = Path.cwd()

            # Extract meeting ID and prepare auth token
            meeting_id = self.extract_meeting_id(url)
            auth_token = self.prepare_auth_token(auth_token)

            print(f"🔍 Meeting ID: {meeting_id}")
            print(f"📁 Output directory: {output_path}")

            # Fetch meeting data
            print("📡 Fetching meeting data...")
            data = self.fetch_meeting_data(meeting_id, auth_token)

            # Parse meeting information
            info = self.parse_meeting_info(data)

            print(f"🎬 Title: {info['name']}")
            print(f"📅 Date: {info['timestamp']}")

            # Prepare output filename
            output_file = output_path / f"{info['timestamp']}_{info['name']}.mp4"

            # Check available downloader
            downloader = self.check_downloader_availability()
            print(f"🔧 Using {downloader['name']} for download")

            # Save metadata
            metadata_name = f"{info['timestamp']}_{info['name']}"
            self.save_metadata(info['full_data'], output_path / metadata_name)

            # Fetch and decode the secured HLS playlist
            print("🔓 Fetching secured playlist...")
            decoded_playlist = self.fetch_decoded_playlist(meeting_id, auth_token)

            with tempfile.NamedTemporaryFile(
                mode='w', suffix='.m3u8', delete=False, encoding='utf-8'
            ) as tmp:
                tmp.write(decoded_playlist)
                playlist_path = Path(tmp.name)

            try:
                if downloader['name'] == 'N_m3u8DL-RE':
                    success = self.download_with_n_m3u8dl_re(playlist_path, output_file)
                else:
                    success = self.download_with_ffmpeg(playlist_path, output_file)
            finally:
                try:
                    playlist_path.unlink()
                except OSError:
                    pass

            if success:
                print(f"\n🎉 Successfully downloaded: {output_file}")
                return str(output_file)
            else:
                print(f"\n💥 Failed to download video")
                return None

        except ValueError as e:
            print(f"❌ Error: {e}")
            return None
        except Exception as e:
            print(f"💥 Unexpected error: {e}")
            return None


def print_instructions():
    """Print detailed instructions for getting auth token"""
    print("""
📋 How to get the Authorization Token:

1. 🌐 Go to https://tldv.io/ and login
2. 📹 Navigate to the meeting you want to download  
3. 🔧 Open Developer Tools (F12 or right-click → Inspect)
4. 🌐 Go to the 'Network' tab
5. 🔄 Refresh the page (F5)
6. 🔍 In the filter box, type: "watch-page"
7. 📡 Look for a request to: "...meetings/.../watch-page?noTranscript=true"
8. 📋 Click on this request → Headers → Request Headers
9. 🔑 Copy the entire "Authorization" value (starts with "Bearer ")

Alternative method:
- Look in Application/Storage → Cookies → Find auth-related cookies
- Or check Local/Session Storage for auth tokens

⚠️  Important Notes:
- The token is session-specific and expires when you log out
- One token can be used for multiple downloads in the same session
- Token typically lasts for the duration of your browser session
- If downloads start failing, get a fresh token by refreshing the page
""")


def parse_urls_from_file(file_path):
    """Parse URLs from a text file (one URL per line)"""
    urls = []
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):  # Skip empty lines and comments
                    urls.append(line)
        return urls
    except Exception as e:
        print(f"❌ Error reading file {file_path}: {e}")
        return []


def main():
    print("🎬 TLDV Video Downloader with N_m3u8DL-RE Support")
    print("=" * 55)

    # Check if help is requested
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        print_instructions()
        return

    downloader = TLDVDownloader()

    try:
        # Check if batch mode is requested
        batch_mode = input("\n📋 Batch download mode? (y/N): ").strip().lower() == 'y'

        if batch_mode:
            # Batch download mode
            print("\n🔄 Batch Download Mode")
            print("You can either:")
            print("1. Enter URLs one by one (type 'done' when finished)")
            print("2. Provide a text file with URLs (one per line)")

            choice = input("\nChoose option (1/2): ").strip()
            urls = []

            if choice == '2':
                file_path = input("📁 Enter path to URLs file: ").strip()
                urls = parse_urls_from_file(file_path)
                if not urls:
                    print("❌ No valid URLs found in file!")
                    return
            else:
                print("\n📎 Enter URLs (type 'done' when finished):")
                while True:
                    url = input("URL: ").strip()
                    if url.lower() == 'done':
                        break
                    if url:
                        urls.append(url)

            if not urls:
                print("❌ No URLs provided!")
                return

            print(f"\n📊 Found {len(urls)} URLs to download")

            # Get auth token (same for all downloads in session)
            print("\n" + "=" * 55)
            print("🔑 Need help getting the auth token? Run with --help flag")
            print("=" * 55)

            auth_token = input("\n🔐 Enter your Authorization token: ").strip()
            if not auth_token:
                print("❌ Authorization token is required!")
                return

            # Optional output directory
            output_dir = input("\n📁 Output directory (press Enter for current): ").strip()
            if not output_dir:
                output_dir = None

            # Parallel workers
            max_workers = input(f"\n🔧 Number of parallel downloads (1-8, default 3): ").strip()
            try:
                max_workers = max(1, min(8, int(max_workers))) if max_workers else 3
            except ValueError:
                max_workers = 3

            # Confirm before download
            print(f"\n📋 Ready for batch download:")
            print(f"   URLs: {len(urls)} videos")
            print(f"   Output: {output_dir or 'Current directory'}")
            print(f"   Parallel workers: {max_workers}")

            confirm = input("\n❓ Proceed with batch download? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Download cancelled by user")
                return

            # Prepare video data list
            video_data_list = [(url, auth_token) for url in urls]

            # Start batch download
            print("\n" + "=" * 55)
            results = downloader.download_multiple_videos(video_data_list, output_dir, max_workers)

            if results:
                print(f"\n🎉 Batch download completed! {len(results)} videos downloaded.")
            else:
                print("\n💥 Batch download failed!")

        else:
            # Single download mode (original behavior)
            url = input("\n📎 Enter the TLDV meeting URL: ").strip()
            if not url:
                print("❌ URL cannot be empty!")
                return

            # Show instructions for getting token
            print("\n" + "=" * 55)
            print("🔑 Need help getting the auth token? Run with --help flag")
            print("=" * 55)

            auth_token = input("\n🔐 Enter your Authorization token: ").strip()
            if not auth_token:
                print("❌ Authorization token is required!")
                return

            # Optional output directory
            output_dir = input("\n📁 Output directory (press Enter for current): ").strip()
            if not output_dir:
                output_dir = None

            # Confirm before download
            print(f"\n📋 Ready to download:")
            print(f"   URL: {url}")
            print(f"   Output: {output_dir or 'Current directory'}")

            confirm = input("\n❓ Proceed with download? (y/N): ").strip().lower()
            if confirm != 'y':
                print("❌ Download cancelled by user")
                return

            # Start download
            print("\n" + "=" * 55)
            result = downloader.download_video(url, auth_token, output_dir)

            if result:
                print(f"\n🎉 All done! Video saved to: {result}")
            else:
                print("\n💥 Download failed!")

    except KeyboardInterrupt:
        print("\n\n⏸️  Download interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")


if __name__ == "__main__":
    main()
