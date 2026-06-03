from BugBusters.pages.profile_page import ProfilePage
from playwright.sync_api import expect
from BugBusters.utils.common_actions import reload_profile_page


def test_successfully_update_first_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    profile_page.first_name.fill("Sandra")
    profile_page.save_button.click()

def test_failed_update_first_name(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_first_name = profile_page.get_first_name_value()
    invalid_first_name = ""

    profile_page.update_name(invalid_first_name)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.first_name).to_have_value(old_first_name)