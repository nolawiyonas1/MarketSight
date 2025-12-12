from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.sql import func
import enum
from .database import Base

# Define possible job statuses
class JobStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Database Model
# This class defines the structure of the "jobs" table in the database
class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)  # Unique ID
    filename = Column(String, index=True)              # Original filename
    file_path = Column(String)                         # Path where file is saved
    status = Column(String, default=JobStatus.PENDING) # Current status
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
