from bughunters.pages import Pages
from bughunters.data.constants import MANAGER_USER


class TestLoginHappyPath:
    def test_successful_login_shows_profile_link(self, pages: Pages) -> None:
        """Happy path: valid credentials → profile link appears in header."""
        pages.auth.login(MANAGER_USER["email"], MANAGER_USER["password"])
        assert pages.auth.is_logged_in(), "Profile link not visible after successful login"


class TestLoginNegative:
    def test_empty_credentials_does_not_login(self, pages: Pages) -> None:
        """Submitting empty form should not authenticate the user."""
        pages.auth.open()
        pages.auth.open_login_modal()
        pages.auth.click_login_submit(force=True)
        assert not pages.auth.is_logged_in(timeout=3000), (
            "Should NOT be logged in with empty credentials"
        )


class TestLogout:
    def test_logout_removes_profile_link(self, auth_pages_ui: Pages) -> None:
        """After logout the profile link must disappear from the header."""
        assert auth_pages_ui.auth.is_logged_in(), "Must be logged in before testing logout"

        auth_pages_ui.personal_info.open()
        auth_pages_ui.personal_info.click_logout()

        auth_pages_ui.auth.wait_until_logged_out(timeout=5000)
