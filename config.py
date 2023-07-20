import os
from dotenv import load_dotenv

load_dotenv()

db_name = os.getenv("DB_NAME")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")