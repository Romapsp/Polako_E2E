import os
from dotenv import load_dotenv

load_dotenv()

class Constants:
    SITE_URL = "https://stg.polakohedonist.club"
    BASE_URL = f"{SITE_URL}/en"

    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("PASSWORD")
    USER_NAME = os.getenv("USER_NAME")
    TIMEOUT = 5000
