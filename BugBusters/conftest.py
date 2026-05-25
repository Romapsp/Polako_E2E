
import os, uuid, pytest

from dotenv import load_dotenv

from BugBusters.app import App
from BugBusters.data.constants import Constants

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


@pytest.fixture
def app(page):
    page.goto(Constants.BASE_URL)
    return App(page)

@pytest.fixture
def base_user_data(app):
    return {
        "name": app.data.USER_NAME,
        "password": app.data.PASSWORD,

    }


@pytest.fixture
def new_user_data(base_user_data):
    return {
        **base_user_data,
        "email": f"qa_user_{uuid.uuid4().hex[:5]}@gmail.com"
    }


@pytest.fixture
def existing_user_data(app, base_user_data):
    return {
        **base_user_data,
        "email": app.data.EMAIL
    }


@pytest.fixture
def login_user_data(app):
    return {
        "email": app.data.EMAIL,
        "password": app.data.PASSWORD,
    }