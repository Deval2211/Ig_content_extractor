#!/usr/bin/env python3
"""
IG Content Extractor - Main Pipeline Orchestrator
Batch process Instagram saved posts into markdown files
"""

import os
import sys
import yaml
import shutil
from pathlib import Path
from extractors.downloader import download_media
from extractors.whisper import transcribe_audio
from extractors.ocr import extract_text_from_image
from ai_writer import generate_markdown

def load_config():
    with open('config.yaml', 'r') as f:
        return yaml.safe_load(f)

def process_url(url, config, collection):
    """Process a single Instagram URL"""
    tmp_dir = Path(config['paths']['tmp'])
    output_dir = Path(config['paths']['output']) / collection
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download media
        media_path, media_type = download_media(url, tmp_dir, config['paths']['cookies'])
        
        # Extract text based on type
        if media_type == 'reel':
            raw_text = transcribe_audio(media_path, config['whisper']['model'])
        else:
            raw_text = extract_text_from_image(media_path)
        
        # Generate markdown
        markdown_content = generate_markdown(raw_text, url, media_type, collection, config)
        
        # Save markdown
        slug = Path(url).stem
        output_path = output_dir / f"{slug}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        # Cleanup
        if media_path and os.path.exists(media_path):
            os.remove(media_path)
        
        print(f"✓ Processed: {url} -> {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Failed: {url} - {e}")
        return False

def main():
    import argparse
    parser = argparse.ArgumentParser(description='IG Content Extractor Pipeline')
    parser.add_argument('--collection', required=True, help='Target collection name')
    parser.add_argument('--urls', default='urls.txt', help='URLs file')
    args = parser.parse_args()
    
    config = load_config()
    
    if not os.path.exists(args.urls):
        print(f"Error: {args.urls} not found")
        sys.exit(1)
    
    with open(args.urls, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Processing {len(urls)} URLs into collection '{args.collection}'")
    
    failed = []
    for url in urls:
        success = False
        for attempt in range(config['processing']['retry_attempts']):
            if process_url(url, config, args.collection):
                success = True
                break
            print(f"  Retry {attempt + 1}/{config['processing']['retry_attempts']}")
        
        if not success:
            failed.append(url)
    
    # Log failures
    if failed:
        with open(config['paths']['failed'], 'w') as f:
            f.write('\n'.join(failed))
        print(f"\n{len(failed)} URLs failed - see {config['paths']['failed']}")
    
    print("\nPipeline complete!")

if __name__ == '__main__':
    main()
