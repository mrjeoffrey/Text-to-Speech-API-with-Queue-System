from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from queue_manager import JobManager
import asyncio
import uuid

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize JobManager
job_manager = JobManager()

class TTSRequest(BaseModel):
    text: str
    voice: str
    pitch: float
    speed: float
    volume: float

@app.post("/tts")
async def tts(request: TTSRequest):
    job_id = str(uuid.uuid4())
    try:
        await job_manager.add_job(job_id, request.dict())
        return {"job_id": job_id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
