import re
from bughunters.pages import Pages

_URL_TIMEOUT = 15_000  # CI runners are slower — give URLs time to settle


class TestPersonalInfoHappyPath:
    def test_page_loads_with_user_email(self, auth_pages: Pages) -> None:
        """Happy path: personal-info page is pre-filled with the authenticated user's email."""
        email = auth_pages.personal_info.get_email()
        assert email and "@" in email, f"Expected valid email, got: {email!r}"

    def test_first_name_field_is_visible(self, auth_pages: Pages) -> None:
        """All profile input fields are present and visible."""
        assert auth_pages.personal_info.are_profile_fields_visible(), (
            "One or more profile fields are not visible"
        )

    def test_profile_url_is_correct(self, auth_pages: Pages) -> None:
        """After login we should land on personal-information, not a login redirect."""
        assert auth_pages.personal_info.current_url_matches(
            re.compile(r"user/personal-information"), timeout=_URL_TIMEOUT,
        ), f"Expected personal-information URL, got: {auth_pages.personal_info.current_url}"

    def test_save_profile_shows_success_feedback(self, auth_pages: Pages) -> None:
        """Happy path: saving the profile stays on the page with no error."""
        current_name = auth_pages.personal_info.get_first_name() or "QA_Bughunter"
        auth_pages.personal_info.update_profile(first_name=current_name)
        assert auth_pages.personal_info.is_save_successful(), (
            "Profile save did not succeed: redirected away or an error appeared"
        )

    def test_all_profile_fields_are_visible(self, auth_pages: Pages) -> None:
        """All expected input fields should be present on the page."""
        assert auth_pages.personal_info.are_profile_fields_visible(), (
            "One or more profile fields are not visible"
        )

    def test_password_change_fields_are_visible(self, auth_pages: Pages) -> None:
        """New password and confirm password fields should be present."""
        assert auth_pages.personal_info.are_password_change_fields_visible(), (
            "Password change fields are not visible"
        )

    def test_sidebar_nav_links_present(self, auth_pages: Pages) -> None:
        """Key sidebar navigation links should be visible."""
        assert auth_pages.personal_info.are_sidebar_links_visible(), (
            "One or more sidebar links are not visible"
        )

    def test_logout_button_is_present(self, auth_pages: Pages) -> None:
        """Logout button should be visible in the sidebar."""
        assert auth_pages.personal_info.is_logout_button_visible(), (
            "Logout button is not visible"
        )


# Navigation + purchases tests need the full UI session — API cookie injection
# does not initialise every Next.js hydration token, so the SPA auth-guard on
# /user/purchases redirects to /ru. These opt in to the UI fallback fixture.
class TestPersonalInfoNavigation:
    def test_navigate_to_purchases_via_sidebar(self, auth_pages_ui: Pages) -> None:
        """navigate_to_purchases() lands on /user/purchases."""
        auth_pages_ui.personal_info.navigate_to_purchases()
        assert "purchases" in auth_pages_ui.purchases.current_url, (
            f"Expected purchases URL, got: {auth_pages_ui.purchases.current_url}"
        )

    def test_navigate_back_to_profile_via_sidebar(self, auth_pages_ui: Pages) -> None:
        """After going to purchases, navigate_to_personal_info() returns to personal-info."""
        auth_pages_ui.personal_info.navigate_to_purchases()
        auth_pages_ui.personal_info.navigate_to_personal_info()
        assert "personal-information" in auth_pages_ui.personal_info.current_url, (
            f"Expected personal-information URL, got: {auth_pages_ui.personal_info.current_url}"
        )


class TestPurchasesPage:
    def test_purchases_page_loads(self, auth_pages_ui: Pages) -> None:
        """Happy path: purchases page is accessible and URL is correct."""
        auth_pages_ui.purchases.open()
        assert "purchases" in auth_pages_ui.purchases.current_url, (
            f"Expected purchases URL, got: {auth_pages_ui.purchases.current_url}"
        )

    def test_purchases_shows_empty_state_or_items(self, auth_pages_ui: Pages) -> None:
        """Purchases page must render either a list or an empty-state message."""
        auth_pages_ui.purchases.open()
        count    = auth_pages_ui.purchases.get_purchase_count()
        is_empty = auth_pages_ui.purchases.is_empty()
        assert count > 0 or is_empty, (
            "Purchases page should show items or an empty-state message"
        )
