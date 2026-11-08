import os
from dotenv import load_dotenv
from pgcraft import connect

load_dotenv(".env")

SECRET_KEY = os.getenv("secret_key")
DB = os.getenv("DB_NAME")
USER = os.getenv("DB_USER")
PASS = os.getenv("DB_PASS")
HOST = os.getenv("DB_HOST")

db = connect(
    host= HOST,
    database= DB,
    user= USER,
    password= PASS
)

