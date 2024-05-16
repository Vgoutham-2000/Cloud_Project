from pydantic import BaseModel
from datetime import date

class JobPosts(BaseModel):
    jobpost_id: int
    job_role: str
    company_name: str
    description: str
    experience: int
    posted_on: date
    location: str
    salary_range: str
    skills: str
    user_id: int

