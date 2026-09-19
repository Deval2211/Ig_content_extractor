# IG Content Pipeline — Technical Architecture

## System Overview

A local Python pipeline that transforms Instagram saved posts into a structured markdown knowledge base.
Media is downloaded temporarily, text is extracted, AI generates the final document, and all media is discarded.

```
┌─────────────────────┐
│  Instagram Saved    │
│  Posts (browser)    │
└──────────┬──────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  IGbulkCollector (Tampermonkey)              │
│  → exports urls.txt                          │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  pipeline.py (orchestrator)                  │
│  - reads urls.txt                            │
│  - loops sequentially                        │
│  - retries up to 5x on failure               │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  extractors/downloader.py                    │
│  - yt-dlp + cookies.txt                      │
│  - downloads to tmp/<id>.<ext>               │
│  - returns file path + detected type         │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  extractors/whisper.py                       │
│  - openai-whisper base model                 │
│  - input: tmp/<id>.mp4                       │
│  - output: raw transcript string             │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  extractors/ocr.py                           │
│  - pytesseract + preprocessing               │
│  - input: tmp/<id>.jpg/.png                  │
│  - output: raw OCR text string               │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  ai_writer.py                                │
│  - prompt: transcript/ocr + url + type       │
│  - AI generates: title, summary, sections,   │
│    key points, suggested collection          │
│  - output: full markdown content             │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  output/collections/<collection>/<slug>.md   │
│  - frontmatter: url, type, date, collection  │
│  - body: AI-generated structured content     │
└──────────┬───────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────────┐
│  cleanup                                     │
│  - delete tmp/<id>.*                         │
│  - log success/failure                       │
└──────────────────────────────────────────────┘
```

---

## Module Details

### pipeline.py
**Responsibility**: Orchestrate the full batch run.

**Flow**:
```
load config
read urls.txt
for each url:
    attempt = 0
    while attempt < 5:
        try:
            media_path, media_type = downloader.download(url)
            if media_type == 'reel':
                raw_text = whisper.transcribe(media_path)
            else:
                raw_text = ocr.extract(media_path)
            markdown = ai_writer.generate(raw_text, url, media_type, collection)
            save_markdown(markdown, collection)
            delete(media_path)
            log_success(url)
            break
        except Exception as e:
            attempt += 1
            if attempt >= 5:
                log_failure(url, e)
```

### extractors/downloader.py
**Responsibility**: Download media temporarily using authenticated yt-dlp.

**Key behaviors**:
- Uses `cookies.txt` exported from browser
- Downloads to `tmp/` with random temp filename
- Returns path + detected type (`reel` or `image`)
- Caller is responsible for cleanup

### extractors/whisper.py
**Responsibility**: Transcribe reel audio to text.

**Key behaviors**:
- Loads Whisper `base` model (configurable)
- Extracts audio from video file
- Returns transcript string
- No diarization, no timestamps — just text

### extractors/ocr.py
**Responsibility**: Extract text from image posts via pytesseract.

**Key behaviors**:
- Opens image with Pillow
- Preprocessing: grayscale, median denoise, autocontrast
- PSM 3 (auto page segmentation)
- Returns extracted text string
- Integrated from your Image_to_text project

### ai_writer.py
**Responsibility**: Send extracted text to AI and generate final markdown.

**Prompt structure**:
```
You are a content archivist. Given the following raw transcript/OCR text from an Instagram post,
generate a well-structured markdown document.

Raw text: {raw_text}
URL: {url}
Type: {reel | image}
Default collection: {collection}

Generate a markdown file with:
1. A clear title
2. A 2-3 sentence summary
3. Key points or concepts (bullet list)
4. The full raw text in a code block
5. Suggested collection (if different from default, explain why)

Output ONLY the markdown content, no explanations.
```

**Output format**:
```markdown
---
url: https://instagram.com/reel/xxx
type: reel
suggested_collection: study
---

# Title

## Summary
...

## Key Points
- ...

## Full Transcript
```
raw text here
```
```

### config.yaml
```yaml
ai:
  provider: openai  # or anthropic, ollama, etc.
  api_key: ${OPENAI_API_KEY}
  model: gpt-4o-mini
  max_retries: 5

whisper:
  model: base  # base, small, medium, large

paths:
  cookies: cookies.txt
  urls: urls.txt
  tmp: tmp/
  output: output/collections/
  failed: output/failed.txt

processing:
  sequential: true
  retry_attempts: 5
```

---

## File Structure

```
igcontent/
├── plan.md
├── architecture.md
├── config.yaml
├── pipeline.py
├── requirements.txt
├── extractors/
│   ├── __init__.py
│   ├── downloader.py
│   ├── whisper.py
│   └── ocr.py
├── ai_writer.py
├── cookies.py
├── output/
│   └── collections/
│       ├── study/
│       ├── entertainment/
│       └── ...
├── tmp/
└── urls.txt
```

---

## Dependencies

```
yt-dlp
openai-whisper
pytesseract
Pillow
PyMuPDF
requests
pyyaml
```

System packages:
- `ffmpeg` (for yt-dlp/Whisper audio processing)
- `tesseract-ocr` (for pytesseract)

---

## Error Handling

- **Download failure**: Retry up to 5x with exponential backoff
- **Transcription failure**: Retry up to 5x
- **OCR failure**: Retry up to 5x
- **AI API failure**: Retry up to 5x, then skip and log
- **Final failure**: Log to `output/failed.txt` with URL + error message
- **Interrupted run**: Pipeline can be restarted; processed URLs are tracked in a checkpoint file

---

## Future Enhancements

- Parallel batch processing with rate limiting
- Incremental runs (skip already-processed URLs)
- Watch mode: auto-process new saved posts
- Vector search over extracted content
- Integration with Obsidian via reels-vault template
