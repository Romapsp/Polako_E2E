from BugBusters.pages.profile_page import ProfilePage
from playwright.sync_api import expect
from BugBusters.utils.common_actions import reload_profile_page

def test_successfully_update_telegram(authorized_page):
    profile_page = ProfilePage(authorized_page)

    telegram_username = "qa_test_user_124"
    expected_telegram = f"@{telegram_username}"

    profile_page.update_telegram(telegram_username)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.telegram).to_have_value(expected_telegram)


def test_failed_update_telegram(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_telegram = profile_page.get_telegram_value()
    invalid_telegram = "not telegram !!!"

    profile_page.update_telegram(invalid_telegram)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.telegram).to_have_value(old_telegram)