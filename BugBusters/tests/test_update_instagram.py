from playwright.sync_api import expect
from BugBusters.pages.profile_page import ProfilePage
from BugBusters.utils.common_actions import reload_profile_page


def test_successfully_update_instagram(authorized_page):
    profile_page = ProfilePage(authorized_page)

    instagram_username = "qa_test_user_124"
    expected_instagram = f"@{instagram_username}"

    profile_page.update_instagram(instagram_username)
    profile_page = reload_profile_page(authorized_page)
    expect(profile_page.instagram).to_have_value(expected_instagram)


def test_failed_update_instagram(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_instagram = profile_page.get_instagram_value()
    invalid_instagram = "not instagram !!!"

    profile_page.update_instagram(invalid_instagram)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.instagram).to_have_value(old_instagram)
