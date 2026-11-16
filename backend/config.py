import os
from dotenv import load_dotenv
from pgcraft import connect

load_dotenv(".env")

SECRET_KEY = os.getenv("secret_key")
allowed_origins = os.getenv("allowed_url")
allow_origins = os.getenv("allow_url")

db = connect(url= os.getenv("DB_URL"))

#DB = os.getenv("DB_NAME")
#USER = os.getenv("DB_USER")
#PASS = os.getenv("DB_PASS")
#HOST = os.getenv("DB_HOST")
#engine = os.getenv("DB_ENGINE")


#db = connect(
#    host= HOST,
#    database= DB,
#    user= USER,
#    password= PASS,
#    engine= engine
#)
