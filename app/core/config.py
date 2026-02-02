import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")
APP_PASSWORD = os.getenv("APP_PASSWORD")
ADMIN_GMAIL = os.getenv("ADMIN_GMAIL")