#!/usr/bin/env python3
"""
OCR module - pytesseract wrapper for image text extraction
"""

from PIL import Image, ImageOps, ImageFilter
import pytesseract

def extract_text_from_image(image_path):
    """Extract text from image using OCR"""
    try:
        # Open and preprocess image
        img = Image.open(image_path)
        
        # Convert to grayscale
        img = ImageOps.grayscale(img)
        
        # Enhance contrast
        img = ImageOps.autocontrast(img)
        
        # Denoise
        img = img.filter(ImageFilter.MedianFilter())
        
        # Extract text
        custom_config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=custom_config)
        
        return text.strip()
        
    except Exception as e:
        raise Exception(f"OCR failed: {e}")
