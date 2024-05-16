import sqlite3

from model.user import User
from dto.user_request import UserRequest
from dto.user_response import UserResponse
from dto.login_credentials import Login
import logging

logging.basicConfig(filename="users.log", encoding='utf-8', filemode='a', level=logging.INFO)
user_logger = logging.getLogger(__name__)

class UserDAO:
    con = sqlite3.connect("revhire.db", check_same_thread=False)
    cursor = con.cursor()

    def create_user(self, user_request: UserRequest):
        user_logger.info(f"user details {user_request}")
        try:
            # Check if the user already exists
            self.cursor.execute(
                """SELECT * FROM USER WHERE email=?""",
                (user_request.email,)
            )
            existing_user = self.cursor.fetchone()
            if existing_user:
                user_logger.info("User already exists")
                raise e("User already exists")

            # If the user doesn't exist, insert the new user
            self.cursor.execute(
                """INSERT INTO USER(name, email, password, role) VALUES(?, ?, ?, ?)""",
                (user_request.name, user_request.email, user_request.password, user_request.role),
            )
            self.con.commit()
            user_logger.info("User created")
            return "created"
        except Exception as e:
            user_logger.error(f"Error in creating new user: {e}")
            raise e("Unable to insert user information")

    
    def get_users(self,user_data:dict):
        self.cursor.execute(
                """SELECT * FROM USER WHERE email=?""",
                (user_data["email"],)
            )
        isuser_permission = self.cursor.fetchone()
        if not isuser_permission:
            user_logger.info("User doesn't exist")
        res = self.cursor.execute(
            """SELECT * from USER"""
        )
        self.con.commit()
        return res.fetchall()
    
    def update_user(self, user_request:UserRequest, id:int):
        self.cursor.execute(
            """UPDATE USER SET name = ?, email = ?, password = ? WHERE id = ?""",(
                user_request.name,user_request.email,user_request.password, id )
        )

        res = self.cursor.execute(
            """SELECT * FROM USER WHERE id = ?""", (id)
        )

        user = res.fetchone()
        self.con.commit()

        user_response = UserResponse(user.id, user.name, user.email, user.role)
        return user_response

    def delete_user(self, id):
        self.cursor.execute("""DELETE FROM USER WHERE id = ?""", (id))
        self.con.commit()
        return "User deleted"
    
    def check_user(self,login: Login):
        try:
            user = self.cursor.execute(
            """SELECT * FROM USER WHERE email=? AND password=?""",(login.email,login.password)
            )
            self.con.commit()
            user_logger.info("user credentials found in table")
            return user.fetchone()
        except Exception as e:
            user_logger.error(f"Error unable to find user : {e}")
            raise e("Error User credentials not found")

    
