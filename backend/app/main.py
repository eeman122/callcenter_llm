from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import os
from dotenv import load_dotenv
from models import process_audio_full  # This would contain your processing logic

app = FastAPI()
port = int(os.environ.get("PORT", 8000))  # Render provides PORT env var

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
    
# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

class AnalysisResult(BaseModel):
    transcription: str
    sentiment: Dict[str, Any]
    tonal: Dict[str, Any]
    evaluation: Dict[str, Any]

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_audio(file: UploadFile = File(...)):
    """Endpoint to process audio files"""
    # Save temporary file
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as f:
        f.write(await file.read())
    
    # Process the file
    result = process_audio_full(temp_path)
    
    # Clean up
    if os.path.exists(temp_path):
        os.remove(temp_path)
    
    return result

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
