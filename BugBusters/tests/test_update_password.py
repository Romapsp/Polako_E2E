from BugBusters.utils.popups import close_whats_new_popup
from BugBusters.pages.profile_page import ProfilePage
from playwright.sync_api import expect
from BugBusters.data.constants import Constants

def test_successfully_update_password(authorized_page):
    profile_page = ProfilePage(authorized_page)

    new_password = "qwertyqwerty2"

    profile_page.new_password.fill(new_password)
    profile_page.confirm_password.fill(new_password)

    expect(profile_page.new_password).to_have_value(new_password)
    expect(profile_page.confirm_password).to_have_value(new_password)

    profile_page.save_button.click()
    authorized_page.wait_for_load_state("networkidle")

    authorized_page.reload()
    authorized_page.wait_for_load_state("networkidle")

    close_whats_new_popup(authorized_page)

    profile_page = ProfilePage(authorized_page)

    expect(profile_page.new_password).to_have_value("")
    expect(profile_page.confirm_password).to_have_value("")


def test_failed_update_password(authorized_page):
    profile_page = ProfilePage(authorized_page)

    new_password = "qwertyqwerty*"
    wrong_confirm_password = "qwertyqwerty1"

    profile_page.new_password.fill(new_password)
    profile_page.confirm_password.fill(wrong_confirm_password)

    expect(profile_page.new_password).to_have_value(new_password)
    expect(profile_page.confirm_password).to_have_value(wrong_confirm_password)

    profile_page.save_button.click()

    authorized_page.wait_for_load_state("networkidle")

    authorized_page.reload()
    authorized_page.wait_for_load_state("networkidle")
    close_whats_new_popup(authorized_page)

    login_response = authorized_page.context.request.post(
        "/api/auth/login",
        data={
            "email": Constants.EMAIL,
            "password": Constants.PASSWORD,
            "mode": "cookie",
        }
    )

    assert login_response.ok, (
        f"Old password stopped working: {login_response.status} {login_response.text()}"
    )