import sqlite3

from model.user import User
from dto.apply_jobrequest import ApplyJobRequest
from dto.change_jobstatus import ChangeJobStatus
# from dto.user_response import UserResponse
import logging

logging.basicConfig(filename="jobstatus.log", encoding='utf-8', filemode='a', level=logging.INFO)
logger_jobstatus = logging.getLogger(__name__)

class JobStatusDAO:
    con = sqlite3.connect("revhire.db", check_same_thread=False)
    cursor = con.cursor()

    def apply_jobpost(self, apply_jobrequest: ApplyJobRequest):
        try:
            self.cursor.execute(
                """INSERT INTO JOBSTATUS(resume_url, status, applied_on, jobpost_id, user_id) VALUES(?, ?, ?, ?, ?)""",
                (  apply_jobrequest.resume_url,  apply_jobrequest.status,  apply_jobrequest.applied_on, apply_jobrequest.jobpost_id, apply_jobrequest.user_id ),
            )
            self.con.commit()
            logger_jobstatus.info("Applied for job post")
            return "applied"
        except Exception as e:
            logger_jobstatus.error(f"Error in applying for new jobpost : {e}")
            raise Exception("unable to apply for jobpost")
        
    def change_jobstatus(self, change_jobstatus: ChangeJobStatus):
        try:
            self.cursor.execute(
                """ UPDATE JOBSTATUS SET status=? WHERE user_id=? AND jobpost_id=? """,(change_jobstatus.status,change_jobstatus.jobseeker_userid,change_jobstatus.jobpost_id)
            )
            self.con.commit()
            logging.info("Job Status dao file")
            return "updated"
        except Exception as e:
            logger_jobstatus.error(f"Error in updating status dao file")
            raise Exception("unable to update jobstatus")

