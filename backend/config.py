import os
from dotenv import load_dotenv
from pgcraft import connect

load_dotenv(".env")

SECRET_KEY = os.getenv("secret_key")
allowed_origins = os.getenv("allowed_url")

db = connect(url= os.getenv("DB_URL"))

