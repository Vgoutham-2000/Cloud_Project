import sqlite3

con = sqlite3.connect('revhire.db')

cursor = con.cursor()


cursor.execute(
    """CREATE TABLE USER(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(20),
        email VARCHAR(20),
        password VARCHAR(20),
        role VARCHAR(20)
    )""")

cursor.execute(
    """ CREATE TABLE JOBPOSTS(
    jobpost_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_role VARCHAR(20),
    company_name VARCHAR(30),
    description VARCHAR(100),
    experience INTEGER,
    posted_on DATE,
    location VARCHAR(50),
    salary_range VARCHAR(30),
    skills VARCHAR(100),
    user_id INTEGER,
    CONSTRAINT fk_USER
    FOREIGN KEY(user_id)
    REFERENCES USER(id)
    )
"""
)
cursor.execute(
    """ CREATE TABLE JOBSTATUS(
    jobstatus_id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_url VARCHAR(70),
    status VARCHAR(15),
    applied_on DATE,
    jobpost_id INTEGER,
    user_id INTEGER,
    CONSTRAINT fk_JOBPOSTS
    FOREIGN KEY (jobpost_id)
    REFERENCES JOBPOSTS(jobpost_id),
    CONSTRAINT fk_USER
    FOREIGN KEY(user_id)
    REFERENCES JOBPOSTS(id)
    )
"""
)

con.commit()

con.close()


