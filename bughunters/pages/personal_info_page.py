from __future__ import annotations
import re
from .base_page import BasePage
from bughunters.data.constants import URLS


class PersonalInfoPage(BasePage):
    _FIRST_NAME       = "input[name='first_name']"
    _LAST_NAME        = "input[name='last_name']"
    _EMAIL            = "input[name='email']"
    _PHONE            = "input[name='phone']"
    _INSTAGRAM        = "input[name='instagram']"
    _TELEGRAM         = "input[name='telegram']"
    _NEW_PASSWORD     = "input[name='new_password']"
    _CONFIRM_PASSWORD = "input[name='confirm_password']"

    # Two submit buttons share the same selector; profile form is the first,
    # password form is the last. Always access via the helpers below.
    _SUBMIT_BTN = "button[type='submit'][data-slot='button']"

    _NAV_PERSONAL_INFO = "a[href*='/user/personal-information']"
    _NAV_PURCHASES     = "a[href*='/user/purchases']"

    _LOGOUT_BTN = "button[type='button'][class*='bg-accent']"

    _PROFILE_FIELDS = ("first_name", "last_name", "email", "phone", "instagram", "telegram")
    _ERROR_LOC = "[role='alert'][class*='error'], [class*='error-message']"

    def open(self) -> None:
        self.navigate(URLS["personal_info"])
        self.close_modal_if_present()

    def get_first_name(self) -> str:
        self.close_modal_if_present()
        return self.page.locator(self._FIRST_NAME).input_value()

    def get_email(self) -> str:
        self.close_modal_if_present()
        return self.page.locator(self._EMAIL).input_value()

    def update_profile(self, first_name: str = None, last_name: str = None,
                       phone: str = None, instagram: str = None, telegram: str = None) -> None:
        self.close_modal_if_present()
        if first_name is not None:
            self.fill(self._FIRST_NAME, first_name)
        if last_name is not None:
            self.fill(self._LAST_NAME, last_name)
        if phone is not None:
            self.fill(self._PHONE, phone)
        if instagram is not None:
            self.fill(self._INSTAGRAM, instagram)
        if telegram is not None:
            self.fill(self._TELEGRAM, telegram)
        self.page.locator(self._SUBMIT_BTN).first.click()

    def navigate_to_purchases(self) -> None:
        self.goto_with_retry(URLS["purchases"], "purchases")

    def navigate_to_personal_info(self) -> None:
        self.goto_with_retry(URLS["personal_info"], "personal-information")

    def click_logout(self) -> None:
        self.close_modal_if_present()
        self.page.locator(self._LOGOUT_BTN).click()

    def change_password(self, new_password: str) -> None:
        self.close_modal_if_present()
        self.fill(self._NEW_PASSWORD, new_password)
        self.fill(self._CONFIRM_PASSWORD, new_password)
        self.page.locator(self._SUBMIT_BTN).last.click()

    # ── State queries (return data; tests do the asserting) ────────────────

    def are_profile_fields_visible(self) -> bool:
        self.close_modal_if_present()
        return all(
            self.page.locator(f"input[name='{n}']").is_visible()
            for n in self._PROFILE_FIELDS
        )

    def are_password_change_fields_visible(self) -> bool:
        self.close_modal_if_present()
        return (
            self.page.locator(self._NEW_PASSWORD).is_visible()
            and self.page.locator(self._CONFIRM_PASSWORD).is_visible()
        )

    def are_sidebar_links_visible(self) -> bool:
        self.close_modal_if_present()
        return (
            self.page.locator(self._NAV_PERSONAL_INFO).first.is_visible()
            and self.page.locator(self._NAV_PURCHASES).first.is_visible()
        )

    def is_logout_button_visible(self) -> bool:
        self.close_modal_if_present()
        return self.page.locator(self._LOGOUT_BTN).is_visible()

    def is_save_successful(self, url_timeout: int = 5_000) -> bool:
        """Profile save succeeded iff we stayed on personal-info and no error appeared."""
        self.close_modal_if_present()
        try:
            self.page.wait_for_url(re.compile(r"user/personal-information"), timeout=url_timeout)
        except Exception:
            return False
        return not self.page.locator(self._ERROR_LOC).is_visible(timeout=2_000)
