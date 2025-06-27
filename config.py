import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")