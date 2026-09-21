#!/usr/bin/env python3
"""
OCR module - pytesseract wrapper for image text extraction
Based on Deval2211/Image_to_text repo preprocessing pipeline
"""

from PIL import Image, ImageFilter, ImageOps
import pytesseract

def preprocess_image(image: Image.Image) -> Image.Image:
    """Gentle cleanup to help OCR - from Image_to_text repo"""
    # Convert to grayscale
    gray = image.convert("L")
    # Light denoise - size=3 is fine for most scans
    denoised = gray.filter(ImageFilter.MedianFilter(size=3))
    # Stretch contrast so dim text becomes darker
    boosted = ImageOps.autocontrast(denoised, cutoff=0.5)
    # Return as RGB for Tesseract
    return boosted.convert("RGB")

def extract_text_from_image(image_path):
    """Extract text from image using OCR with Image_to_text preprocessing"""
    try:
        # Open image
        img = Image.open(image_path).convert("RGB")
        
        # Preprocess using Image_to_text pipeline
        cleaned = preprocess_image(img)
        
        # Extract text with PSM 3 for fully automatic page segmentation
        # Handles columns, mixed layouts better than PSM 6
        custom_config = r'--oem 3 --psm 3'
        text = pytesseract.image_to_string(
            cleaned, 
            lang='eng', 
            config=custom_config
        )
        
        return text.strip()
        
    except Exception as e:
        raise Exception(f"OCR failed: {e}")
