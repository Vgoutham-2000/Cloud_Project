from pydantic import BaseModel

class JobStatus(BaseModel):
    jobstatus_id: int
    resume_url: str
    status: str
    applied_on: str
    jobpost_id: int
    user_id: int