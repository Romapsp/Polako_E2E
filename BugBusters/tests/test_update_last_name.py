from playwright.sync_api import expect

from BugBusters.pages.profile_page import ProfilePage
from BugBusters.utils.common_actions import reload_profile_page


def test_successfully_update_last_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    new_last_name = "Test"

    profile_page.update_last_name(new_last_name)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.last_name).to_have_value(new_last_name)


def test_failed_update_last_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_last_name = profile_page.get_last_name_value()
    invalid_last_name = ""

    profile_page.update_last_name(invalid_last_name)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.last_name).to_have_value(old_last_name)