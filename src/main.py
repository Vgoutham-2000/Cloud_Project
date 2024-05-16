from fastapi import FastAPI, HTTPException
import logging
import jwt
from user_service import UserService
from jobposts_service import JobPostsService
from jobstatus_service import JobStatusService
from dto.user_request import UserRequest
from dto.user_response import UserResponse
from dto.login_credentials import Login
from dto.create_jobrequest import JobPosts
from dto.apply_jobrequest import ApplyJobRequest
from dto.change_jobstatus import ChangeJobStatus
import os
from dotenv import load_dotenv
from dto.job_response import JobPosts 

logging.basicConfig(filename="user_controller.log", encoding='utf-8', filemode='a', level=logging.INFO)

logger=logging.getLogger(__name__)
load_dotenv()
app = FastAPI()


@app.get("/")
def welcome():
    return "welcome to Revhire"

@app.get("/users")
def get_users(user_jwt:str,user_service = UserService()):
    try:
        
        users_data = user_service.get_users(user_jwt)
        logger.info("User data retreived")
        return users_data, 200
    
    except Exception:
        logger.error("failed to retrieve data")
        raise HTTPException(status_code=500, detail="failed to retrieve data")

@app.post("/signup")
def create_user(user_request:UserRequest):
    try:
        user_service = UserService()
        user_service.create_user(user_request)
        logger.info("User Created")
        return "user created"
    except Exception:
        logger.error("failed to create user")
        raise HTTPException(status_code=500, detail="failed to create user")

@app.post("/login")
def login(login:Login):
    try:
        user_service = UserService()
        user_data = user_service.check_user(login)
        if user_data:
            (user_id,name,email,password,role) = user_data
            return jwt.encode({"email": email,"role": role,"user_id":user_id,"name":name}, os.getenv('secret'), algorithm="HS256") # payload,key,alg
    except Exception:
        logger.error("failed to login")
        return HTTPException(status_code=404, detail="failed to login")
    
@app.post("/createjobpost")
def createjobpost(create_jobrequest:JobPosts, user_jwt: str):
    try:
        jobpost = JobPostsService()
        jobpost.create_jobpost(create_jobrequest,user_jwt)
        logger.info("Job post Created")
        return "job post created"
    except Exception:
        logger.error("failed to create job post")
        return HTTPException(status_code=404, detail="failed to create job post")
    
@app.get('/allposts')
def fetchalljobposts(user_jwt: str):
    try:
        jobpost = JobPostsService()
        return jobpost.fetchall_jobposts(user_jwt)
    except Exception:
        logger.error("failed to fetch job posts")
        return HTTPException(status_code=500, detail="unable to fetch job posts")

@app.get('/allposts/{user_id}')
def fetchalljobposts_employer(user_id : int, user_jwt: str):
    try:
        jobpost = JobPostsService()
        return jobpost.fetchall_jobposts_employer(user_id, user_jwt)
    except Exception:
        logger.error("")
        return HTTPException(status_code=500, detail="unable to fetch jobposts of employer")

@app.post('/applyjob')
def applyjob(apply_jobrequest: ApplyJobRequest, user_jwt: str):
    try:
        jobstatus_service = JobStatusService()
        jobstatus_service.apply_jobpost(apply_jobrequest, user_jwt)
        logger.info("Applied for job post")
        return "applied for job post"
    except Exception:
        logger.error("failed to apply for jobpost")
        return HTTPException(status_code=404, detail="failed to apply for job post")
    
@app.patch('/changejobstatus')
def changestatus(change_jobstatus: ChangeJobStatus, user_jwt: str):
    try:
        jobstatus_service = JobStatusService()
        jobstatus_service.change_jobstatus(change_jobstatus, user_jwt)
        logger.info("Job status updated")
        return "job status updated"
    except Exception:
        logger.error("failed in updating job status")
        return HTTPException(status_code=404, detail="failed to update job status")

        














