from playwright.sync_api import expect

from BugBusters.pages.profile_page import ProfilePage
from BugBusters.data.constants import Constants
from BugBusters.utils.common_actions import reload_profile_page


def test_email_is_displayed_correctly(authorized_page):
    profile_page = ProfilePage(authorized_page)

    expect(profile_page.email).to_have_value(Constants.EMAIL)


def test_failed_update_email(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_email = profile_page.get_email_value()
    invalid_email = "not-email"

    profile_page.update_email(invalid_email)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.email).to_have_value(old_email)
