from TP_Polako_E2E.base.base_test import BaseTest
from TP_Polako_E2E.pages.auth.login_page import (
    LOGIN_FORM,
)
from TP_Polako_E2E.utils.constants import (
    EMPTY_PASSWORD,
    INVALID_PASSWORD,
    SQL_INJECTION_PAYLOAD,
    TEST_EMAIL,
    INVALID_EMAIL,
    VALID_TEST_PASSWORD,
    XSS_PAYLOAD,
    INVALID_EMAIL_WITHOUT_AT, UNREGISTERED_EMAIL,
)


class TestLogin(BaseTest):

    def test_login_success(self):
        self.login_page.login_and_go_to_profile()
        self.manager_profile.close_modal()

        self.user_profile.verify_logout_button_visible()

    def test_login_with_token(self, authenticated_page):
        self.manager_profile.close_modal()
        self.user_profile.verify_logout_button_visible()

    def test_login_with_empty_password(self):
        self.login_page.open_login_modal()
        self.login_page.fill_login_form(
            TEST_EMAIL
        )

        assert self.login_page.is_login_button_disabled()

    def test_login_with_invalid_password(self):
        self.login_page.open_login_modal()
        self.login_page.fill_login_form(TEST_EMAIL, INVALID_PASSWORD[0])
        self.login_page.click_login_button()

        self.login_page.verify_error_message()

    def test_login_with_unregistered_email(self):
        self.login_page.open_login_modal()

        self.login_page.login(

            INVALID_EMAIL,
            VALID_TEST_PASSWORD
        )

        self.login_page.verify_error_message()

    def test_login_with_email_without_at_symbol(self):
        self.login_page.open_login_modal()

        self.login_page.login(

            INVALID_EMAIL_WITHOUT_AT,
            VALID_TEST_PASSWORD,

        )

        self.login_page.verify_error_message()

    def test_login_with_email_ending_at_symbol(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            "test@",
            VALID_TEST_PASSWORD,
        )

        self.login_page.verify_error_message()

    def test_login_with_email_without_local_part(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            "@gmail.com",
            VALID_TEST_PASSWORD,
        )

        self.login_page.verify_error_message()

    def test_login_with_email_without_at_separator(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            "test.gmail.com",
            VALID_TEST_PASSWORD,
        )

        self.login_page.verify_error_message()

    def test_login_with_email_without_valid_domain(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            "test@com",
            VALID_TEST_PASSWORD,
        )

        self.login_page.verify_error_message()

    def test_login_sql_injection(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            SQL_INJECTION_PAYLOAD,
            SQL_INJECTION_PAYLOAD,
        )

        self.login_page.verify_error_message()

    def test_login_xss_attempt(self):
        self.login_page.open_login_modal()

        self.login_page.login(
            XSS_PAYLOAD,
            XSS_PAYLOAD,
        )

        self.login_page.verify_error_message()

    def test_login_modal_is_displayed(self):
        self.login_page.open_login_modal()

        assert self.login_page.is_visible(LOGIN_FORM)

