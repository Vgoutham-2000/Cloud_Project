from pydantic import BaseModel
from datetime import date

class ApplyJobRequest(BaseModel):
    resume_url: str
    status: str
    applied_on: date
    jobpost_id: int
    user_id: int
