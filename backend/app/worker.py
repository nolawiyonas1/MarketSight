import time
import os
import boto3
from .database import SessionLocal
from . import models, crud, ml

# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

def upload_to_s3(file_path, object_name):
    """Uploads a file to an S3 bucket."""
    if not S3_BUCKET:
        print("Worker: S3_BUCKET_NAME not set. Skipping upload.")
        return False
        
    s3_client = boto3.client('s3', region_name=AWS_REGION)
    try:
        print(f"Worker: Uploading {file_path} to S3 bucket {S3_BUCKET}...")
        s3_client.upload_file(file_path, S3_BUCKET, object_name)
        print("Worker: Upload successful.")
        return f"s3://{S3_BUCKET}/{object_name}"
    except Exception as e:
        print(f"Worker: S3 Upload failed: {e}")
        return False

def train_model(job_id: int):
    """
    Trains a model using PyTorch and uploads the result to S3.
    """
    print(f"Worker: Starting job #{job_id}")
    
    # 1. Connect to DB
    db = SessionLocal()
    
    try:
        # 2. Get the job
        job = crud.get_job(db, job_id)
        if not job:
            print(f"Worker: Job {job_id} not found!")
            return

        # 3. Update status to PROCESSING
        job.status = models.JobStatus.PROCESSING
        db.commit()
        
        # 4. Real Training
        print(f"Worker: Training model for {job.filename}...")
        
        # Define where to save the model locally first
        model_filename = f"model_{job_id}.pth"
        local_model_path = f"uploads/{model_filename}"
        
        # Run the training logic
        ml.train(job.file_path, local_model_path)
        
        # 5. Upload to S3 (if configured)
        s3_path = upload_to_s3(local_model_path, model_filename)
        
        # 6. Update status to COMPLETED
        job.status = models.JobStatus.COMPLETED
        # Optionally save the S3 path in the DB if you add a column for it later
        # job.model_url = s3_path 
        
        db.commit()
        print(f"Worker: Job #{job_id} completed successfully.")
        
    except Exception as e:
        print(f"Worker: Error processing job {job_id}: {e}")
        job.status = models.JobStatus.FAILED
        db.commit()
    finally:
        db.close()
