# IG Content Pipeline — Project Plan

## Goal
Turn your Instagram saved posts into a searchable knowledge base of extracted content.
No media files stored — only AI-generated markdown files with transcripts, OCR text, summaries, and smart organization.

---

## What We're Building

A batch pipeline that:
1. Collects URLs from your Instagram saved posts
2. Downloads each post/reel temporarily
3. Extracts text via Whisper (reels) or pytesseract OCR (images)
4. Sends raw text to an AI model to generate a structured markdown file
5. Saves the markdown into collection-organized folders
6. Deletes all media files — only text remains

---

## Workflow

### Phase 1 — URL Collection
- Install IGbulkCollector Tampermonkey script
- Open Instagram saved posts in browser
- Click Start → Export URL list → `urls.txt`
- Output: flat list of `/p/` and `/reel/` URLs

### Phase 2 — Cookie Export
- One-time export of logged-in browser cookies to `cookies.txt`
- Needed for yt-dlp to access Instagram without login walls

### Phase 3 — Batch Extraction
- Run `pipeline.py` with target collection name
- For each URL:
  - Download media with yt-dlp + cookies
  - Detect type (reel vs image post)
  - Extract text:
    - Reel → Whisper transcription
    - Image → pytesseract OCR
  - Send text + URL + type to AI writer
  - AI generates final markdown file
  - Save to `output/collections/<collection>/<slug>.md`
  - Delete media file
- Retry failed items up to 5 times
- Sequential processing (one at a time)
- Log failures to `output/failed.txt`

### Phase 4 — AI Tagging & Organization
- AI suggests collection based on content
- If content clearly belongs to a different collection, AI moves/suggests move
- You can manually override collection in markdown frontmatter

---

## What We Need to Create

| File/Dir | Purpose |
|----------|---------|
| `plan.md` | This file |
| `architecture.md` | Technical architecture |
| `config.yaml` | API keys, model selection, default collection, paths |
| `pipeline.py` | Main orchestrator — loops through URLs, runs extraction |
| `extractors/whisper.py` | Whisper transcription wrapper |
| `extractors/ocr.py` | pytesseract OCR wrapper (from your Image_to_text logic) |
| `extractors/downloader.py` | yt-dlp wrapper for temporary media download |
| `ai_writer.py` | LLM prompt + API call, generates final markdown |
| `cookies.py` | Browser cookie export utility |
| `output/collections/` | Generated markdown files organized by collection |
| `output/failed.txt` | Failed URLs for manual review |
| `tmp/` | Temporary media storage (cleared after each item) |

---

## Forks/Extensions

### IGbulkCollector
- Use as-is for URL collection
- No code changes needed
- Install via Tampermonkey

### reels-vault
- Reference for yt-dlp + Whisper integration patterns
- Fork if we need to modify download behavior
- Currently single-reel CLI; we need batch mode

---

## Dependencies

- Python 3.10+
- yt-dlp
- openai-whisper
- pytesseract + tesseract-ocr system package
- Pillow
- PyMuPDF (fitz)
- requests/httpx (for AI API calls)

---

## Decisions Made

| Decision | Choice |
|----------|--------|
| Transcription | Whisper (local, free, open-source) |
| OCR | pytesseract (from your Image_to_text project) |
| AI for structuring | API-based (you'll provide key) |
| Media storage | Temporary only — delete after extraction |
| Collection assignment | You specify default + AI can suggest override |
| Processing mode | Sequential |
| Retry policy | 5 attempts per URL |
| Output format | Markdown files, one per post/reel |

## Decisions Pending

| Decision | Options |
|----------|---------|
| AI provider | OpenAI / Anthropic / local Ollama / other |
| Prompt style | Structured JSON → markdown vs freeform |
| Whisper model size | base / small / medium / large |

---

## Next Steps

1. Create architecture.md with full technical design
2. Scaffold project structure
3. Build extractors (whisper, ocr, downloader)
4. Build AI writer with prompt template
5. Build pipeline orchestrator
6. Test with 3-5 sample URLs
7. Iterate on prompt/output format
