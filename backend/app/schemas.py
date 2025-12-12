from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import JobStatus

# Pydantic models define the structure of request/response data (Validation)

# Base fields shared by creating and reading
class JobBase(BaseModel):
    filename: str

# Fields needed when creating a job (internal use)
class JobCreate(JobBase):
    file_path: str

# Fields returned to the API user (Reading)
class Job(JobBase):
    id: int
    status: JobStatus
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        # Allows Pydantic to read data from SQLAlchemy models
        orm_mode = True
