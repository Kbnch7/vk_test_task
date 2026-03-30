import os
import logging

from dotenv import load_dotenv

load_dotenv()

def setup_logger():
    logging.basicConfig(
        filemode='a',
        filename='mylog.log',
        format="%(asctime)s %(levelname)s %(message)s",
        level=logging.DEBUG
    )

DATABASE_URL = os.getenv("DATABASE_URL")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
PASSWORD_ENCRYPTION_KEY = os.getenv("PASSWORD_ENCRYPTION_KEY")
DATABASE_NAME = os.getenv("DATABASE_NAME")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
print(f"DEBUG: DATABASE_URL is {os.getenv('DATABASE_URL')}")
