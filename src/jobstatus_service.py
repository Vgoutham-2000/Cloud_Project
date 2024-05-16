from jobstatus_dao import JobStatusDAO
from dto.apply_jobrequest import ApplyJobRequest
from dto.change_jobstatus import ChangeJobStatus
import os
import jwt
from dotenv import load_dotenv
import logging

logging.basicConfig(filename="jobstatus.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger_jobstatus = logging.getLogger(__name__)
load_dotenv()

class JobStatusService:
    def apply_jobpost(self, apply_jobrequest: ApplyJobRequest, user_jwt ):
        try:
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            if user_info["role"] != "Jobseeker":
                raise Exception("User don't have permission")
            jobstatus_dao = JobStatusDAO()
            return jobstatus_dao.apply_jobpost(apply_jobrequest)
        except Exception as e:
            logger_jobstatus.error(f"Unable to apply for job post {e}")
            raise Exception("Unable to apply for job post")
        
    def change_jobstatus(self,change_jobstatus: ChangeJobStatus, user_jwt):
        try:
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            if user_info["role"] != "Employer":
                raise Exception("User don't have permission")
            jobstatus_dao = JobStatusDAO()
            return jobstatus_dao.change_jobstatus(change_jobstatus)
        except Exception as e:
            logger_jobstatus.error(f"unable to update jobstatus {e}")
            raise Exception("Unable to update job status")
        