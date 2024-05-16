from pydantic import BaseModel

class ChangeJobStatus(BaseModel):
    status: str
    jobpost_id: int
    jobseeker_userid: int