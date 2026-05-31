import os
from dotenv import load_dotenv

load_dotenv()

class Constants:
    BASE_URL = os.getenv("BASE_URL")
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    USER_NAME = os.getenv("USER_NAME")
    TIMEOUT = 5000