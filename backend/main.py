import os
import shutil
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from typing import Optional

# Import our services
from download_manager import download_video
from highlight_detector import analyze_highlights
from video_editor import create_summary

app = FastAPI(title="Video Transformer API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure output directory exists before mounting
os.makedirs("output", exist_ok=True)
app.mount("/static", StaticFiles(directory="output"), name="static")

class VideoRequest(BaseModel):
    url: str
    target_duration: Optional[int] = 60  # seconds
    style: Optional[str] = "energetic" # energetic, balanced, chill

class ProcessStatus(BaseModel):
    status: str
    progress: int
    message: str
    result_path: Optional[str] = None

# In-memory storage for job status (database would be better for prod)
jobs = {}

@app.post("/api/process")
async def process_video(request: VideoRequest, background_tasks: BackgroundTasks):
    job_id = str(len(jobs) + 1)
    jobs[job_id] = {
        "status": "queued",
        "progress": 0,
        "message": "Job queued",
        "result_path": None
    }
    
    background_tasks.add_task(run_processing_pipeline, job_id, request.url, request.target_duration)
    
    return {"job_id": job_id}

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]

async def run_processing_pipeline(job_id: str, url: str, target_duration: int):
    try:
        # 1. Download
        jobs[job_id].update({"status": "downloading", "progress": 10, "message": "Downloading video..."})
        video_path = download_video(url, download_dir="temp_downloads")
        
        # 2. Analyze
        jobs[job_id].update({"status": "analyzing", "progress": 40, "message": "Analyzing audio levels for highlights..."})
        cuts = analyze_highlights(video_path, target_duration)
        
        if not cuts:
             raise Exception("No highlights found or video too short.")

        # 3. Edit
        jobs[job_id].update({"status": "editing", "progress": 80, "message": "Stitching clips together..."})
        output_path = create_summary(video_path, cuts, output_dir="output")

        jobs[job_id].update({"status": "completed", "progress": 100, "message": "Processing complete!", "result_path": output_path})
        
        # Cleanup original download? 
        # os.remove(video_path) 
        
    except Exception as e:
        jobs[job_id].update({"status": "failed", "progress": 0, "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    # Ensure directories exist
    os.makedirs("temp_downloads", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    uvicorn.run(app, host="0.0.0.0", port=8000)
