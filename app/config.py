import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
PASSWORD_ENCRYPTION_KEY = os.getenv("PASSWORD_ENCRYPTION_KEY")
print(f"DEBUG: DATABASE_URL is {os.getenv('DATABASE_URL')}")
