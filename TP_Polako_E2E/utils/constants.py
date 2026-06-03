import os
import re
import string

from pathlib import Path
from dotenv import load_dotenv
import uuid
import random

load_dotenv()
EMAIL_ADDRESS = os.getenv("VALID_EMAIL")


SECTIONS_MAPPING = {
    "events": "#events",
    "prices": "pricing",
    "tickets": "https://polako-tickets.rs/index-ru.html",
    "certificates": "services",
    "news": "news",
    "about": "about",
    "analytics": "analytics",
}


EXPECTED_MARKERS = {
    "telegram": "t.me/polakohedonist",
    "instagram_ru": "instagram.com/polakohedonist/",
    "instagram_sr": "instagram.com/polakohedonist.dogadjaji",
    "email": "mailto:support@polakohedonist.rs",
    "viber": "viber://chat",
    "whatsapp": "whatsapp.com",
}


# LoginPage


INVALID_EMAIL_WITHOUT_AT = "test3mail.com"
TEST_EMAIL = "test3@mail.com"
INVALID_PASSWORD = "WrongPassword123"
INVALID_EMAIL = "not_exist@test.com"


TEST_EMAIL = "test3@mail.com"

UNREGISTERED_EMAIL = "not_exist@test.com"
VALID_TEST_PASSWORD = "Password123"
SQL_INJECTION_PAYLOAD = "' OR 1=1 --"
XSS_PAYLOAD = "<script>alert(1)</script>"
EXPECTED_ERROR_TEXT = "Неверный логин или пароль"
EMPTY_PASSWORD = ""
INVALID_EMAILS = [
    "test",
    "test@",
    "@gmail.com",
    "test.gmail.com",
    "test@com",
]

EVENT_NAME = "test_event"
EVENT_DESCRIPTION = "test_description"
EVENT_LOCATION = "Test Location (NS)"
EVENT_DURATION = "60"
EVENT_COST = "100"
EVENT_TO_DELETE = EVENT_NAME
ROOT_DIR = Path(__file__).resolve().parent.parent
IMAGE_PATH = ROOT_DIR / "test_data" / "test_events_foto.png"
TITLE_TEXT_RESULT = "The event title is empty."
EXPECTED_EMAIL_FORMAT_ERROR_MESSAGE = "При обновлении пароля произошла ошибка. Попробуйте еще раз."
TEST_NAME = "test_name"
VALID_COMPANY_NAME = "Valid Company Name"
LONG_COMPANY_NAME = "A" * 101
EXPECTED_ERROR_TEXT_COMPANY_NAME = "Ошибка: Максимальная длина 100 символов"


def generate_random_email(domain: str = "test.com") -> str:
    unique_id = uuid.uuid4().hex[:8]
    return f"testuser_{unique_id}@{domain}"


def generate_random_user_name() -> str:
    unique_id = uuid.uuid4().hex[:6]
    return f"TestUser_{unique_id}"


def generate_random_company_name() -> str:
    unique_id = uuid.uuid4().hex[:6]
    return f"TestCompany_{unique_id}"


def generate_random_password(length: int = 12) -> str:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for i in range(length))
    return password

VALID_PROFILE_DATA = {
    "first_name": "Ramses",
    "last_name": "Fourth",
    "email": "sergioodessit+1@gmail.com",
    "phone": "+1234567890",
    "instagram": "@ramsey",
    "telegram": "@ram4",
}

PARTIAL_PROFILE_DATA = {
    "first_name": "Привет",
    "last_name": "",
    "email": "hello@icloud.com",
    "phone": "",
    "instagram": "",
    "telegram": "@hello",
}

INVALID_PROFILE_DATA = {
    "first_name": "932c- mv3c kmf in0 \[w [wld][mcna]чьэцуст0ш3ьц0ч3 932c- mv3c kmf in0 \[w [wld][mcna]чьэцуст0ш3ьц0ч3",
    "last_name": "932c- mv3c kmf in0 \[w [wld][mcna]чьэцуст0ш3ьц0ч3 932c- mv3c kmf in0 \[w [wld][mcna]чьэцуст0ш3ьц0ч3",
    "email": """onetwo+simullteniesly.twentyfive-seventyday_samountqwertyuiopasdfghjklzxcvbnmqwertyuiopasdfghjklzxcvbnm
    qwertyuiopasdfg@gmail.com""",
    "phone": """+123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012
    3456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567
    8901234567890123456789012345678901234""",
    "instagram": """Пейзик!([#}{2@'%"/|^34*.,`~""",
    "telegram": "ауцтсту.92ьх3ь-!смзц@",
}


VALID_NEW_PASSWORD = "t1T!k@cK%"
INVALID_NEW_PASSWORD = ""



VALID_NEW_PASSWORD = "t1T!k@cK%"


INVALID_PASSWORD = [
    "WrongPassword123",
    "OR 1=1; DROP TABLE users;",
    "<script>alert(1)</script>",
    "Passمرحبا123שלוםword",
    "${jndi:ldap://127.0.0.1/a}",
    "%s%s%s%s%s%s%s%s%s%s%s%n%d" * 500,
    ""
]

random_email = generate_random_email()
random_user_name = generate_random_user_name()
random_company_name = generate_random_company_name()
random_password = generate_random_password()

VALID_RANDOM_USERS_DATA = [
    random_email,
    random_user_name,
    random_company_name,
    random_password,
]

HOME_PAGE_REGEXP = re.compile(r".*/(ru|sr|en)?(#events)?$")
APP_STORE_REGEXP = re.compile(r"apps\.apple\.com/.*/app/polako-hedonist/id6745751830")
GOOGLE_PLAY_REGEXP = re.compile(r"play\.google\.com/store/apps/details\?id=blue\.muffin\.polako\.client")
