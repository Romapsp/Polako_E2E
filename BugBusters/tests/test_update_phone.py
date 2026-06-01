import pytest

from BugBusters.pages.profile_page import ProfilePage
from playwright.sync_api import expect
from BugBusters.utils.common_actions import reload_profile_page


@pytest.mark.skip(
    reason="Тест в разработке"
)
def test_successfully_update_phone(authorized_page):
    profile_page = ProfilePage(authorized_page)

    new_phone = "+49123456789"

    profile_page.update_phone(new_phone)

    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.phone).to_have_value("+49123456789")

@pytest.mark.skip(
    reason="Тест в разработке"
)
def test_failed_update_phone(authorized_page):
    profile_page = ProfilePage(authorized_page)

    old_phone = profile_page.phone.input_value()
    invalid_phone = "abc123"

    profile_page.update_phone(invalid_phone)
    profile_page = reload_profile_page(authorized_page)

    expect(profile_page.phone).to_have_value(old_phone)

