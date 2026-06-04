from __future__ import annotations
from .base_page import BasePage
from bughunters.data.constants import URLS


class AuthPage(BasePage):
    _LOGIN_HEADER_BTN = "button.ml-4"
    _EMAIL    = "input[name='email']"
    _PASSWORD = "input[name='password']"
    _SUBMIT   = "button[type='submit'].btn-accent"
    _ERROR    = "[role='alert'], [class*='error'], [class*='Error']"

    _REGISTER_LINK   = "button.underline"
    _REG_FOR_USER    = "button.btn-accent:nth-of-type(1)"
    _REG_FOR_MANAGER = "button.btn-accent:nth-of-type(2)"

    _FIRST_NAME = "input[name='firstName'], input[name='first_name']"
    _LAST_NAME  = "input[name='lastName'],  input[name='last_name']"
    _REG_SUBMIT = "button[type='submit'].btn-accent"

    def open(self) -> None:
        self.navigate(URLS["home"])

    def open_login_modal(self) -> None:
        self._click_login_button()
        self.wait_visible(self._EMAIL)

    def login(self, email: str, password: str) -> None:
        self.open()
        self.open_login_modal()
        self.fill(self._EMAIL, email)
        self.fill(self._PASSWORD, password)
        self.click_login_submit()

    def click_login_submit(self, force: bool = False) -> None:
        """Click the login form submit button. ``force=True`` bypasses the
        actionability check (useful for negative tests on a disabled button)."""
        self.page.locator(self._SUBMIT).first.click(force=force)

    def get_error_message(self) -> str:
        loc = self.page.locator(self._ERROR)
        return loc.inner_text() if loc.is_visible() else ""

    def open_register_user(self) -> None:
        self.open()
        self.open_login_modal()
        self.click(self._REGISTER_LINK)
        self.page.locator("button.btn-accent").first.click()

    def open_register_manager(self) -> None:
        self.open()
        self.open_login_modal()
        self.click(self._REGISTER_LINK)
        self.page.locator("button.btn-accent").nth(1).click()

    def register_user(
        self, first_name: str, last_name: str, email: str, password: str
    ) -> None:
        self.open_register_user()
        self.fill(self._FIRST_NAME, first_name)
        self.fill(self._LAST_NAME, last_name)
        self.fill(self._EMAIL, email)
        self.fill(self._PASSWORD, password)
        self.click(self._REG_SUBMIT)
