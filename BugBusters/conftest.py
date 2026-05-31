from playwright.sync_api import Page
import os, uuid, pytest
from dotenv import load_dotenv

from BugBusters.app import App
from BugBusters.data.constants import Constants
from BugBusters.utils.popups import close_whats_new_popup

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))


@pytest.fixture(autouse=True)
def app(page: Page):
    page.goto(Constants.BASE_URL)

    yield App(page)


@pytest.fixture(scope="session")
def browser_type_launch_args():
    return {
        "headless": False,
        "slow_mo": 1500,
    }


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


@pytest.fixture
def authorized_page(browser, login_user_data):
    context = browser.new_context(
        base_url=Constants.SITE_URL,
        extra_http_headers={
            "Origin": Constants.SITE_URL,
            "Referer": Constants.BASE_URL,
        }
    )

    login_response = context.request.post(
        "/api/auth/login",
        data={
            "email": login_user_data["email"],
            "password": login_user_data["password"],
            "mode": "cookie",
        }
    )

    assert login_response.ok, (
        f"Login failed: {login_response.status} {login_response.text()}"
    )

    access_token = login_response.json()["data"]["access_token"]

    page = context.new_page()

    page.goto(Constants.BASE_URL)
    page.evaluate(
        """token => {
            localStorage.setItem("access_token", token);
            localStorage.setItem("token", token);
        }""",
        access_token
    )

    page.goto(f"{Constants.BASE_URL}/user/personal-information")
    page.wait_for_load_state("networkidle")

    close_whats_new_popup(page)

    print("AUTHORIZED PAGE URL:", page.url)

    yield page

    context.close()
        "name": app.data.USER_NAME,
    }
