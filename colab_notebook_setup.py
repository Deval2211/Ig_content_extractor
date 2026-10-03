#!/usr/bin/env python3
"""
IG Content Extractor - Colab Ready Notebook
Run this notebook in Google Colab to extract Instagram content
"""

import os
import sys
from pathlib import Path

# Setup paths
os.makedirs('/content/tmp', exist_ok=True)
os.makedirs('/content/output/collections', exist_ok=True)

print("=" * 60)
print("IG Content Extractor - Colab Ready")
print("=" * 60)
print("\n1. Install dependencies")
print("2. Setup project")
print("3. Extract content")
