import os
import re
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
import torchaudio
from pydub import AudioSegment

# Audio Processing Utilities
def convert_to_wav(audio_path: str) -> str:
    """Convert any audio file to WAV format.
    
    Args:
        audio_path: Path to input audio file
        
    Returns:
        Path to converted WAV file
    """
    output_path = os.path.splitext(audio_path)[0] + ".wav"
    audio = AudioSegment.from_file(audio_path)
    audio.export(output_path, format="wav")
    return output_path

def resample_audio(audio_path: str, target_sample_rate: int = 16000) -> Tuple[str, int]:
    """Resample audio to target sample rate.
    
    Args:
        audio_path: Path to input audio file
        target_sample_rate: Target sample rate (default 16kHz)
        
    Returns:
        Tuple of (output_path, original_sample_rate)
    """
    waveform, sample_rate = torchaudio.load(audio_path)
    if sample_rate == target_sample_rate:
        return audio_path, sample_rate
    
    output_path = os.path.join(tempfile.gettempdir(), f"resampled_{Path(audio_path).name}")
    resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sample_rate)
    resampled_waveform = resampler(waveform)
    torchaudio.save(output_path, resampled_waveform, target_sample_rate)
    return output_path, sample_rate

# Text Processing Utilities
def clean_transcript_text(text: str) -> str:
    """Clean raw transcript text."""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Standardize speaker labels
    text = re.sub(r'(SPEAKER|SPK)_?(\d+)', r'Speaker \2', text, flags=re.IGNORECASE)
    return text

def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT-style timestamp."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}"

# File Utilities
def save_temp_file(file_bytes: bytes, extension: str = "") -> str:
    """Save bytes to temporary file with optional extension.
    
    Args:
        file_bytes: File content as bytes
        extension: File extension (e.g., '.wav')
        
    Returns:
        Path to temporary file
    """
    temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    temp_file.write(file_bytes)
    temp_file.close()
    return temp_file.name

def cleanup_files(*file_paths: str) -> None:
    """Clean up temporary files."""
    for path in file_paths:
        try:
            if path and os.path.exists(path):
                os.unlink(path)
        except Exception as e:
            print(f"Error deleting file {path}: {e}")

# JSON Utilities
def safe_json_loads(json_str: str) -> Optional[Dict[str, Any]]:
    """Safely parse JSON string with fallback."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # Try to extract JSON from malformed strings
        match = re.search(r'\{.*\}', json_str, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return None

# Speaker Label Validation
def validate_speaker_labels(labels: Dict[str, str]) -> bool:
    """Validate speaker labels conform to expected format."""
    required_keys = {"Agent", "Customer"}
    return all(
        key in labels 
        and isinstance(labels[key], str) 
        and labels[key] in required_keys
        for key in labels
    )

# Environment Utilities
def check_required_env_vars() -> None:
    """Check required environment variables are set."""
    required_vars = {
        "ASSEMBLYAI_API_KEY",
        "GROQ_API_KEY",
        "HUGGINGFACE_API_TOKEN"
    }
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")