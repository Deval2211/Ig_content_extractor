# OCR module - Image_to_text integration README

## Source Repository
https://github.com/Deval2211/Image_to_text

## Integration Details

The OCR extractor now uses preprocessing pipeline from your Image_to_text repo:

### Preprocessing Pipeline
1. **Grayscale conversion** - `image.convert("L")`
2. **Denoising** - `MedianFilter(size=3)` for light noise removal
3. **Contrast enhancement** - `ImageOps.autocontrast(cutoff=0.5)` to make dim text darker
4. **RGB conversion** - Back to RGB for Tesseract compatibility

### OCR Configuration
- **OEM**: 3 (Default + LSTM)
- **PSM**: 3 (Fully automatic page segmentation, handles columns/mixed layouts)
- **Language**: eng

### Why PSM 3 vs PSM 6?
- PSM 3: Handles arbitrary layouts, columns, mixed orientations
- PSM 6: Assumes single uniform block of text
- Instagram posts often have mixed layouts → PSM 3 is better

### Files Updated
- `extractors/ocr.py` - Integrated Image_to_text preprocessing

### Usage
```python
from extractors.ocr import extract_text_from_image

text = extract_text_from_image('/path/to/image.jpg')
```

Same API as before, but with better preprocessing quality from your proven pipeline.
