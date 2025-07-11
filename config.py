import os
import logging
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s]: %(asctime)s - %(name)s - %(message)s",
)
