from typing import Callable

from TP_Polako_E2E.base.base_page import BasePage

PROFILE_BTN = 'nav a[href*="personal-information"]'
PURCHASES_BTN = 'nav a[href*="purchases"]'
BALANCE_BTN = 'nav a[href*="balance"]'

USER_ROLE_BADGE = "nav ~ div div.gap-1 span"
LOGOUT_BTN = "main div.rounded-2xl button"

BASIC_INFO = "form:has(#first_name) > p:nth-of-type(1)"
FIRST_NAME_INPUT = "#first_name"
LAST_NAME_INPUT = "#last_name"

CONTACT_INFO = "form:has(#first_name) > p:nth-of-type(2)"
EMAIL_INPUT = "#email"
PHONE_INPUT = "#phone"
INSTAGRAM_INPUT = "#instagram"
TELEGRAM_INPUT = "#telegram"

SAVE_PROFILE_BTN = 'form:has(#first_name) button[type="submit"]'

CHANGE_PASSWORD = "main form:nth-of-type(2) > p"
NEW_PASSWORD_INPUT = "#new_password"
CONFIRM_PASSWORD_INPUT = "#confirm_password"
CHANGE_PASSWORD_BTN = 'main form:nth-of-type(2) button[type="submit"]'


class UserProfilePage(BasePage):
    # SIDEBAR
    def click_profile_btn(self):
        self.page.locator(PROFILE_BTN).click()

    def click_purchase_history_btn(self):
        self.page.locator(PURCHASES_BTN).click()

    def click_balance_btn(self):
        self.page.locator(BALANCE_BTN).click()

    def verify_profile_btn_visible(self, timeout: int = 3000):
        self.page.locator(PROFILE_BTN).wait_for(state="visible", timeout=timeout)

    def verify_purchase_history_btn_visible(self, timeout: int = 3000):
        self.page.locator(PURCHASES_BTN).wait_for(state="visible", timeout=timeout)

    def verify_balance_btn_visible(self, timeout: int = 3000):
        self.page.locator(BALANCE_BTN).wait_for(state="visible", timeout=timeout)

    # PROFILE INFORMATION
    def verify_user_role_badge(self):
        self.page.locator(USER_ROLE_BADGE).wait_for(state="visible", timeout=4000)

    def click_logout(self):
        self.page.locator(LOGOUT_BTN).click()

    def verify_logout_button_visible(self):
        self.page.locator(LOGOUT_BTN).wait_for(state="visible", timeout=4000)

    # MANAGE PROFILE
    # First Name
    def verify_first_name_visible(self, timeout: int = 3000):
        self.page.locator(FIRST_NAME_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_first_name(self, value: str):
        self.page.locator(FIRST_NAME_INPUT).fill(value)

    def get_first_name_value(self) -> str:
        return self.page.locator(FIRST_NAME_INPUT).input_value()

    # Last Name
    def verify_last_name_visible(self, timeout: int = 3000):
        self.page.locator(LAST_NAME_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_last_name(self, value: str):
        self.page.locator(LAST_NAME_INPUT).fill(value)

    def get_last_name_value(self) -> str:
        return self.page.locator(LAST_NAME_INPUT).input_value()

    # Email
    def verify_email_visible(self, timeout: int = 3000):
        self.page.locator(EMAIL_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_email(self, value: str):
        self.page.locator(EMAIL_INPUT).fill(value)

    def get_email_value(self) -> str:
        return self.page.locator(EMAIL_INPUT).input_value()

    # Phone
    def verify_phone_visible(self, timeout: int = 3000):
        self.page.locator(PHONE_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_phone(self, value: str):
        self.page.locator(PHONE_INPUT).fill(value)

    def get_phone_value(self) -> str:
        return self.page.locator(PHONE_INPUT).input_value()

    # Instagram
    def verify_instagram_visible(self, timeout: int = 3000):
        self.page.locator(INSTAGRAM_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_instagram(self, value: str):
        self.page.locator(INSTAGRAM_INPUT).fill(value)

    def get_instagram_value(self) -> str:
        return self.page.locator(INSTAGRAM_INPUT).input_value()

    # Telegram
    def verify_telegram_visible(self, timeout: int = 3000):
        self.page.locator(TELEGRAM_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_telegram(self, value: str):
        self.page.locator(TELEGRAM_INPUT).fill(value)

    def get_telegram_value(self) -> str:
        return self.page.locator(TELEGRAM_INPUT).input_value()

    # Full data
    def fill_all_profile_fields(self, profile_data: dict[str, str]):
        fill_methods: dict[str, Callable[[str], None]] = {
            "first_name": self.fill_first_name,
            "last_name": self.fill_last_name,
            "email": self.fill_email,
            "phone": self.fill_phone,
            "instagram": self.fill_instagram,
            "telegram": self.fill_telegram,
        }

        for key, fill_func in fill_methods.items():
            value = profile_data.get(key)
            if value is not None:
                fill_func(value)

    def get_all_profile_values(self) -> dict:
        return {
            "first_name": self.get_first_name_value(),
            "last_name": self.get_last_name_value(),
            "email": self.get_email_value(),
            "phone": self.get_phone_value(),
            "instagram": self.get_instagram_value(),
            "telegram": self.get_telegram_value(),
        }

    def click_save_profile(self):
        with self.page.expect_response(
            lambda response: "user" in response.url or "profile" in response.url
        ) as response_info:
            self.page.click("button[type='submit']")

        assert response_info.value.status in [
            200,
            201,
        ], f"The backend returned an error while saving: {response_info.value.status}"

    # CHANGE PASSWORD
    # NEW PASSWORD
    def verify_new_password_visible(self, timeout: int = 3000):
        self.page.locator(NEW_PASSWORD_INPUT).wait_for(state="visible", timeout=timeout)

    def fill_new_password(self, value: str):
        self.page.locator(NEW_PASSWORD_INPUT).fill(value)

    # CONFIRM PASSWORD
    def verify_confirm_password_visible(self, timeout: int = 3000):
        self.page.locator(CONFIRM_PASSWORD_INPUT).wait_for(
            state="visible", timeout=timeout
        )

    def fill_confirm_password(self, value: str):
        self.page.locator(CONFIRM_PASSWORD_INPUT).fill(value)

    # BUTTON CHANGE PASSWORD
    def verify_change_password_btn_visible(self, timeout: int = 3000):
        self.page.locator(CHANGE_PASSWORD_BTN).wait_for(
            state="visible", timeout=timeout
        )

    def click_change_password(self):
        self.page.locator(CHANGE_PASSWORD_BTN).click()

    def change_password(
        self, new_pass: str, confirm_pass: str, expected_status: int | None = 200
    ):
        if new_pass is not None:
            self.fill_new_password(new_pass)
        if confirm_pass is not None:
            self.fill_confirm_password(confirm_pass)

        if expected_status is None:
            self.click_change_password()
            return None

        with self.page.expect_response(
            lambda response: "password" in response.url, timeout=10000
        ) as response_info:
            self.click_change_password()

        actual_status = response_info.value.status

        if expected_status == 200:
            assert actual_status in [
                200,
                204,
            ], f"A successful password reset was expected, but the backend returned a code: {actual_status}"
        else:
            assert (
                actual_status == expected_status
            ), f"An error code was expected {expected_status}, but the backend returned a code: {actual_status}"

        return response_info.value
