import time
from .database import SessionLocal
from . import models, crud

def train_model(job_id: int):
    """
    Simulates training a model.
    This function runs in the background worker.
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
        
        # 4. Simulate Training (Wait 5 seconds)
        # TODO: Phase 3 - Replace this sleep with actual PyTorch training logic
        print(f"Worker: Training model for {job.filename}...")
        time.sleep(5)
        
        # 5. Update status to COMPLETED
        job.status = models.JobStatus.COMPLETED
        db.commit()
        print(f"Worker: Job #{job_id} completed successfully.")
        
    except Exception as e:
        print(f"Worker: Error processing job {job_id}: {e}")
        job.status = models.JobStatus.FAILED
        db.commit()
    finally:
        db.close()
