#!/usr/bin/env python3
"""
Whisper transcription module
"""

import whisper

def transcribe_audio(audio_path, model_size='base'):
    """Transcribe audio/video using Whisper"""
    try:
        model = whisper.load_model(model_size)
        result = model.transcribe(audio_path)
        return result['text']
    except Exception as e:
        raise Exception(f"Transcription failed: {e}")
