import os
import shutil
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud, database

# Create tables if they don't exist
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="MarketSight API")

# Helper to get DB session
get_db = database.get_db

# Ensure upload directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def read_root():
    return {"message": "Welcome to MarketSight API"}

@app.post("/upload/", response_model=schemas.Job)
def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Uploads a file and creates a background job."""
    file_location = f"{UPLOAD_DIR}/{file.filename}"
    
    # 1. Save file to disk
    # TODO: In production, upload this to AWS S3 instead of local disk
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # 2. Save job info to DB
    job_data = schemas.JobCreate(filename=file.filename, file_path=file_location)
    job = crud.create_job(db=db, job=job_data)
    
    return job

@app.get("/jobs/{job_id}", response_model=schemas.Job)
def read_job(job_id: int, db: Session = Depends(get_db)):
    """Get status of a specific job."""
    db_job = crud.get_job(db, job_id=job_id)
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job

@app.get("/jobs/", response_model=List[schemas.Job])
def read_jobs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all jobs."""
    jobs = crud.get_jobs(db, skip=skip, limit=limit)
    return jobs
