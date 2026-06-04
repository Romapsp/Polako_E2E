import os
from dotenv import load_dotenv


load_dotenv()

BASE_URL        = "https://stg-client.polakohedonist.club"
BASE_URL_AUTH   = "https://stg.polakohedonist.club"
LANG = "ru"

URLS = {
    "home":           f"{BASE_URL}/{LANG}",
    "login":          f"{BASE_URL}/{LANG}",
    "personal_info":  f"{BASE_URL_AUTH}/{LANG}/user/personal-information",
    "purchases":      f"{BASE_URL_AUTH}/{LANG}/user/purchases",
    "events":         f"{BASE_URL_AUTH}/{LANG}/events",
    "events_create":  f"{BASE_URL_AUTH}/{LANG}/user/events/create",
    "events_list":    f"{BASE_URL_AUTH}/{LANG}/user/events",
    "reports":        f"{BASE_URL_AUTH}/{LANG}/user/reports",
}

TIMEOUTS = {
    "default":    30_000,
    "navigation": 60_000,
    "element":    10_000,
}

_email    = os.getenv("EMAIL")
_password = os.getenv("PASSWORD")
if not _email or not _password:
    raise RuntimeError(
        "EMAIL and PASSWORD must be set in .env or environment variables"
    )
MANAGER_USER = {"email": _email, "password": _password}

NEW_USER = {
    "email":      "test_user_{}@example.com",
    "password":   "TestUser123!",
    "first_name": "Test",
    "last_name":  "User",
}

EVENT_DATA = {
    "title":       "Playwright Auto Event",
    "description": "Created by automation",
    "date":        "2027-01-15",
    "time":        "19:00",
    "location":    "Belgrade",
    "capacity":    "100",
}
