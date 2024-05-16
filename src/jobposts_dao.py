import sqlite3

from model.user import User
from dto.create_jobrequest import JobPosts
# from dto.user_response import UserResponse
import logging

logging.basicConfig(filename="job_posts.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger_jobpostservice = logging.getLogger(__name__)

class JobPostsDAO:
    con = sqlite3.connect("revhire.db", check_same_thread=False)
    cursor = con.cursor()

    def create_jobpost(self, job_post:JobPosts):
        logger_jobpostservice.info(f"job post details {job_post}")
        try:
            self.cursor.execute(
                """INSERT INTO JOBPOSTS(job_role, company_name, description, experience, posted_on, location, salary_range,skills, user_id) VALUES(?, ?, ?,?,?,?,?,?,?)""",
                (  job_post.job_role,  job_post.company_name,  job_post.description,  job_post.experience,  job_post.posted_on,  job_post.location,  job_post.salary_range, job_post.skills,  job_post.user_id ),
            )
            self.con.commit()
            logging.info("Job post created")
            return "created"
        except Exception as e:
            logging.error(f"Error in creating new job post : {e}")
            raise Exception("unable to insert job info")

    
    def fetchall_jobposts(self,user_info: dict):
        self.cursor.execute(
                """SELECT * FROM USER WHERE email=?""",
                (user_info["email"],)
            )
        isuser_permission = self.cursor.fetchone()
        if not isuser_permission:
            logger_jobpostservice.info("User doesn't exist")
            raise Exception("Authentication failed")
        res = self.cursor.execute(
            """SELECT * from JOBPOSTS"""
        )
        self.con.commit()
        return res.fetchall()
    
    def fetchall_jobposts_employer(self,employer_id):
        res = self.cursor.execute(
            """SELECT * from JOBPOSTS WHERE user_id = ? """,(employer_id,)
        )
        self.con.commit()
        return res.fetchall()