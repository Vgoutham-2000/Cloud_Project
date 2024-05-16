from jobposts_dao import JobPostsDAO
from dto.create_jobrequest import JobPosts
import os
import jwt
from dotenv import load_dotenv
import logging

logging.basicConfig(filename="job_posts.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger_jobpostservice = logging.getLogger(__name__)
load_dotenv()

class JobPostsService:
    def create_jobpost(self, jobpost: JobPosts, user_jwt: str):
        try:
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            if user_info["role"] != "Employer":
                raise e("User don't have permission")
            jobpost_dao = JobPostsDAO()
            return jobpost_dao.create_jobpost(jobpost)
        except Exception as e:
            logger_jobpostservice.error(f"Unable to create jobpost {e}")
            raise e(f"Unable to create jobpost {e}")
        
    def fetchall_jobposts(self,user_jwt: str):
        try:
            jobpost_dao = JobPostsDAO()
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            return jobpost_dao.fetchall_jobposts(user_info)
        except Exception as e:
            logger_jobpostservice.error(f"Unable to fetch all jobposts {e}")
            raise e("Unable to fetch all jobposts")
        
    def fetchall_jobposts_employer(self, employer_id, user_jwt):
        try:
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            if user_info["role"] != "Employer":
                raise e("User don't have permission")
            jobpost_dao = JobPostsDAO()
            return jobpost_dao.fetchall_jobposts_employer(employer_id)
        except Exception as e:
            logger_jobpostservice.error(f"Unable to fetch all jobposts of employer {e}")
            raise  e("Unable to fetch all jobposts of employer")
    