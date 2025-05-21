from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class SpeakerSegment(BaseModel):
    start: float
    end: float
    speaker: str
    text: str

class SentimentResult(BaseModel):
    label: str
    score: float

class TonalResult(BaseModel):
    Neutral: Optional[float] = Field(0.0, ge=0, le=1)
    Negative: Optional[float] = Field(0.0, ge=0, le=1)

class EvaluationMetrics(BaseModel):
    Resolution: int = Field(..., ge=1, le=10)
    Compliance: int = Field(..., ge=1, le=10)
    Satisfaction: int = Field(..., ge=1, le=10)
    Final_rating: float = Field(..., ge=1, le=10)
    Evaluation: str

class AnalysisResponse(BaseModel):
    """Full analysis response model"""
    transcription: str
    segments: List[SpeakerSegment]
    sentiment: Dict[str, SentimentResult]  # Keys: "Agent", "Customer", "Overall"
    tonal: Dict[str, TonalResult]         # Keys: "Agent", "Customer", "Overall"
    evaluation: EvaluationMetrics
    language: Optional[str]
    num_speakers: Optional[int]

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    details: Optional[str] = None
    status_code: int

# Request models
class AudioAnalysisRequest(BaseModel):
    """Payload for audio analysis request"""
    audio_url: Optional[str] = None  # Alternative to file upload
    min_speakers: Optional[int] = Field(1, ge=1, le=10)
    max_speakers: Optional[int] = Field(2, ge=1, le=10)