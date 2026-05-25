import pytest
import os
from dotenv import load_dotenv

from BugBusters.data.constants import Constants

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

from BugBusters.pages.login_page import LoginPage
from BugBusters.pages.registration_page import RegistrationPage
from BugBusters.pages.personal_info_page import PersonalInfoPage
from BugBusters.pages.purchase_page import PurchasePage
from BugBusters.pages.event_pages import EventCreatePage, EventEditPage
from BugBusters.pages.profile_page import ProfilePage


# OopCompanion:suppressRename


class App:
    def __init__(self, page):
        self.page = page
        self.auth = LoginPage(page)
        self.data = Constants
        self.registration = RegistrationPage(page)
        self.personal_info = PersonalInfoPage(page)
        self.purchases = PurchasePage(page)
        self.event_create = EventCreatePage(page)
        self.event_edit = EventEditPage(page)
        self.profile = ProfilePage(page)

@pytest.fixture
def app(page):
    page.goto(Constants.BASE_URL)
    return App(page)