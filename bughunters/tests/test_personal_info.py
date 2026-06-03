import re
from playwright.sync_api import expect
from bughunters.pages import Pages


class TestPersonalInfoHappyPath:
    def test_page_loads_with_user_email(self, auth_pages: Pages) -> None:
        """Happy path: personal-info page is pre-filled with the authenticated user's email."""
        email = auth_pages.personal_info.get_email()
        assert email and "@" in email, f"Expected valid email, got: {email!r}"

    def test_first_name_field_is_visible(self, auth_pages: Pages) -> None:
        """First name input should be present and visible."""
        auth_pages.personal_info.verify_profile_fields_visible()

    def test_profile_url_is_correct(self, auth_pages: Pages) -> None:
        """After API login we should land on personal-information, not a login redirect."""
        expect(auth_pages.personal_info.page).to_have_url(
            re.compile(r"user/personal-information")
        )

    def test_save_profile_shows_success_feedback(self, auth_pages: Pages) -> None:
        """Happy path: saving the profile stays on the page with no error."""
        current_name = auth_pages.personal_info.get_first_name() or "QA_Bughunter"
        auth_pages.personal_info.update_profile(first_name=current_name)
        auth_pages.personal_info.verify_save_succeeded()


    def test_all_profile_fields_are_visible(self, auth_pages: Pages) -> None:
        """All expected input fields should be present on the page."""
        auth_pages.personal_info.verify_profile_fields_visible()

    def test_password_change_fields_are_visible(self, auth_pages: Pages) -> None:
        """New password and confirm password fields should be present."""
        auth_pages.personal_info.verify_password_fields_visible()

    def test_sidebar_nav_links_present(self, auth_pages: Pages) -> None:
        """Key sidebar navigation links should be visible."""
        auth_pages.personal_info.verify_sidebar_links_visible()

    def test_logout_button_is_present(self, auth_pages: Pages) -> None:
        """Logout button should be visible in the sidebar."""
        auth_pages.personal_info.verify_logout_btn_visible()


class TestPersonalInfoNavigation:
    def test_navigate_to_purchases_via_sidebar(self, auth_pages: Pages) -> None:
        """Clicking the purchases sidebar link navigates to /user/purchases."""
        auth_pages.personal_info.navigate_to_purchases()
        expect(auth_pages.personal_info.page).to_have_url(re.compile(r"user/purchases"))

    def test_navigate_back_to_profile_via_sidebar(self, auth_pages: Pages) -> None:
        """After going to purchases, clicking profile link returns to personal-info."""
        auth_pages.personal_info.navigate_to_purchases()
        auth_pages.personal_info.navigate_to_personal_info()
        expect(auth_pages.personal_info.page).to_have_url(
            re.compile(r"user/personal-information")
        )


class TestPurchasesPage:
    def test_purchases_page_loads(self, auth_pages: Pages) -> None:
        """Happy path: purchases page is accessible."""
        auth_pages.purchases.open()
        expect(auth_pages.purchases.page).to_have_url(re.compile(r"user/purchases"))

    def test_purchases_shows_empty_state_or_items(self, auth_pages: Pages) -> None:
        """Purchases page must render either a list or an empty-state message."""
        auth_pages.purchases.open()
        count    = auth_pages.purchases.get_purchase_count()
        is_empty = auth_pages.purchases.is_empty()
        assert count > 0 or is_empty, (
            "Purchases page should show items or an empty-state message"
        )
