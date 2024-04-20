from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Sample data storage (replace with a database in production)
class Database:
    job_seekers = {}
    employers = {}
    jobs = {}


class Job(BaseModel):
    title: str
    company: str
    location: str
    experience_years: int


class JobApplication(BaseModel):
    job_id: str
    job_seeker_id: str


class JobApplicationStatus(BaseModel):
    job_id: str
    status: str  # 'shortlisted' or 'rejected'


# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to RevHire API. Visit /docs for documentation."}


# Job Seeker Endpoints
@app.post("/job-seekers/register/")
def register_job_seeker(job_seeker_id: str):
    Database.job_seekers[job_seeker_id] = {}
    return {"message": "Job seeker registered successfully"}


@app.post("/job-seekers/login/")
@app.get("/job-seekers/login/")
def login_job_seeker(job_seeker_id: str):
    if job_seeker_id not in Database.job_seekers:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    return {"message": "Job seeker logged in successfully"}



@app.get("/job-seekers/search/")
def search_jobs(job_role: Optional[str] = None, location: Optional[str] = None, experience_years: Optional[int] = None, company_name: Optional[str] = None):
    # Filtering jobs based on provided parameters
    filtered_jobs = []
    for job_id, job_details in Database.jobs.items():
        if (not job_role or job_details['title'] == job_role) and \
           (not location or job_details['location'] == location) and \
           (not experience_years or job_details['experience_years'] == experience_years) and \
           (not company_name or job_details['company'] == company_name):
            filtered_jobs.append({job_id: job_details})
    return {"jobs": filtered_jobs}


@app.post("/job-seekers/apply/")
def apply_for_job(application: JobApplication):
    job_id = application.job_id
    job_seeker_id = application.job_seeker_id
    if job_id not in Database.jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    if job_seeker_id not in Database.job_seekers:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    # Store application details
    Database.job_seekers[job_seeker_id][job_id] = "applied"
    return {"message": "Job application submitted successfully"}


@app.get("/job-seekers/applications/")
def get_applications(job_seeker_id: str):
    if job_seeker_id not in Database.job_seekers:
        raise HTTPException(status_code=404, detail="Job seeker not found")
    return Database.job_seekers[job_seeker_id]


# Employer Endpoints
@app.post("/employers/register/")
def register_employer(employer_id: str):
    Database.employers[employer_id] = {}
    return {"message": "Employer registered successfully"}


@app.post("/employers/login/")
def login_employer(employer_id: str):
    if employer_id not in Database.employers:
        raise HTTPException(status_code=404, detail="Employer not found")
    return {"message": "Employer logged in successfully"}


@app.post("/employers/post-job/")
def post_job(job: Job, employer_id: str):
    job_id = len(Database.jobs) + 1
    Database.jobs[job_id] = job.dict()
    Database.employers[employer_id][job_id] = []
    return {"message": "Job posted successfully"}


@app.get("/employers/applications/")
def get_applications_for_job(job_id: str, employer_id: str):
    if employer_id not in Database.employers:
        raise HTTPException(status_code=404, detail="Employer not found")
    if job_id not in Database.jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return Database.employers[employer_id].get(job_id, [])


@app.post("/employers/process-application/")
def process_job_application(status: JobApplicationStatus):
    job_id = status.job_id
    employer_id = status.employer_id
    if employer_id not in Database.employers:
        raise HTTPException(status_code=404, detail="Employer not found")
    if job_id not in Database.jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    if status.status not in ['shortlisted', 'rejected']:
        raise HTTPException(status_code=400, detail="Invalid status")
    # Update application status
    Database.employers[employer_id][job_id].append({job_id: status.status})
    return {"message": "Application status updated successfully"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
