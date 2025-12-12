from sqlalchemy.orm import Session
from . import models, schemas

# CRUD = Create, Read, Update, Delete

def create_job(db: Session, job: schemas.JobCreate):
    """Creates a new job in the database."""
    db_job = models.Job(
        filename=job.filename,
        file_path=job.file_path,
        status=models.JobStatus.PENDING
    )
    db.add(db_job)      # Add to session
    db.commit()         # Save to DB
    db.refresh(db_job)  # Reload to get ID and defaults
    return db_job

def get_job(db: Session, job_id: int):
    """Fetch a single job by ID."""
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    """Fetch a list of jobs."""
    return db.query(models.Job).offset(skip).limit(limit).all()
