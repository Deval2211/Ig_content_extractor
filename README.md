# IG Content Extractor

A batch pipeline that transforms Instagram saved posts into a searchable knowledge base of markdown files.

## Overview

This tool extracts all your saved Instagram posts (reels and images), converts the content to text, and generates structured markdown files — all organized by collection.

**Key feature**: Media files are downloaded temporarily and deleted after extraction. Only the text content remains.

---

## Quick Start

### 1. Collect URLs

Install the [IGbulkCollector](https://github.com/doncezart/IGbulkCollector) Tampermonkey script:

1. Install Tampermonkey extension in your browser
2. Add the script from URL:
   ```
   https://raw.githubusercontent.com/doncezart/IGbulkCollector/main/instagram-saved-collector.user.js
   ```
3. Open Instagram → Your Profile → Saved posts
4. Click the **▶ Start** button in the IG Bulk Collector panel
5. Click **⤓ Export .txt** to download `urls.txt`

### 2. Export Browser Cookies

1. Install `cookies-extras` extension in Chrome/Edge/Firefox
2. Go to `chrome://settings/cookies` → "Export cookies"
3. Save as `cookies.txt` in the project root

### 3. Configure AI Provider

Edit `config.yaml`:

```yaml
ai:
  provider: openai
  api_key: "your-api-key-here"
  model: gpt-4o-mini
```

### 4. Run the Pipeline

```bash
python pipeline.py --collection study
```

The pipeline will:
- Download each URL temporarily
- Transcribe reels with Whisper
- Extract text from images with OCR
- Generate markdown via AI
- Save to `output/collections/study/`
- Delete all media files

---

## Project Structure

```
igcontent/
├── plan.md              # Development roadmap
├── architecture.md      # Technical design
├── README.md            # This file
├── config.yaml          # Configuration
├── urls.txt             # URL list from IGbulkCollector
├── cookies.txt          # Browser cookies
├── pipeline.py          # Main entry point
├── requirements.txt     # Python dependencies
├── extractors/          # Media/text extraction modules
│   ├── downloader.py
│   ├── whisper.py
│   └── ocr.py
├── ai_writer.py         # AI markdown generator
├── output/              # Generated markdown files
│   └── collections/
└── tmp/                 # Temporary media (auto-cleaned)
```

---

## Configuration

`config.yaml` controls:

```yaml
ai:
  provider: openai
  api_key: "your-openai-key"
  model: gpt-4o-mini
  max_retries: 5

whisper:
  model: base  # base, small, medium, large

paths:
  cookies: cookies.txt
  urls: urls.txt
  tmp: tmp/
  output: output/collections/

processing:
  sequential: true
  retry_attempts: 5
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Download fails | Make sure you're logged into Instagram; re-export cookies |
| Rate limited | Wait and retry; Instagram blocks aggressive downloads |
| AI API errors | Check your API key and quota |
| OCR poor quality | Tesseract works best with clear, high-contrast text |

---

## Related Projects

- [IGbulkCollector](https://github.com/doncezart/IGbulkCollector) — URL collection
- [reels-vault](https://github.com/Overusedhydra/reels-vault) — Reference implementation
- [Image_to_text](https://github.com/Deval2211/Image_to_text) — OCR logic

---

## License

MIT — use freely, create your own knowledge base.