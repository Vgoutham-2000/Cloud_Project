from user_dao import UserDAO
from dto.user_request import UserRequest
from dto.login_credentials import Login
import logging
from dotenv import load_dotenv
import os
import jwt

logging.basicConfig(filename="users.log", encoding='utf-8', filemode='a', level=logging.INFO)
user_logger = logging.getLogger(__name__)
load_dotenv() #searches for .env file and loads env variables

class UserService:
    def get_users(self,user_jwt):
        try:
            user_info = jwt.decode(user_jwt, os.getenv('secret') , algorithms=["HS256"])
            user_dao = UserDAO()
            return user_dao.get_users(user_info)
        except Exception as e:
            user_logger.error(f"User credentials not found {e}")
            raise e(" Unable to find user")
        
    def create_user(self, user_request:UserRequest):
        try:
            user_dao = UserDAO()
            return user_dao.create_user(user_request)
        except Exception as e:
            user_logger.error("Unable to create user in UserService")
            raise e("Unable to create user")
        
    def check_user(self, login: Login):
        try:
            user_dao = UserDAO()
            user_service_data = user_dao.check_user(login)
            if user_service_data:
                return user_service_data
            else:
                user_logger.error("User credentials not found ")
                raise e(" Unable to find user 1")
        except Exception as e:
            user_logger.error(f"User credentials not found {e}")
            raise e(" Unable to find user")
            
