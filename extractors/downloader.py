#!/usr/bin/env python3
"""
Downloader module - yt-dlp wrapper for Instagram media
"""

import os
import tempfile
from pathlib import Path
import yt_dlp

def download_media(url, tmp_dir, cookies_path):
    """Download Instagram media temporarily"""
    tmp_dir = Path(tmp_dir)
    tmp_dir.mkdir(parents=True, exist_ok=True)
    
    # Determine media type from URL
    media_type = 'reel' if '/reel/' in url else 'image'
    
    # Setup yt-dlp options
    ydl_opts = {
        'format': 'best[ext=mp4]' if media_type == 'reel' else 'best[ext=jpg]',
        'outtmpl': str(tmp_dir / '%(id)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
    }
    
    if os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Ensure file exists
            if not os.path.exists(filename):
                # Try alternative naming
                for ext in ['mp4', 'jpg', 'jpeg', 'png']:
                    alt_path = str(tmp_dir / f"{info.get('id', 'media')}.{ext}")
                    if os.path.exists(alt_path):
                        filename = alt_path
                        break
            
            return filename, media_type
            
    except Exception as e:
        raise Exception(f"Download failed: {e}")
