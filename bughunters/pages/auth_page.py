from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS, TIMEOUTS


class AuthPage(BasePage):
    # ── Login modal ───────────────────────────────────────────────────────
    _LOGIN_HEADER_BTN = "button.ml-4"
    _EMAIL    = "input[name='email']"
    _PASSWORD = "input[name='password']"
    _SUBMIT   = "button[type='submit'].btn-accent"
    _ERROR    = "[role='alert'], [class*='error'], [class*='Error']"

    _PROFILE_LINK = "header a[href*='/user']"

    # ── Registration flow ─────────────────────────────────────────────────
    _REGISTER_LINK   = "button.underline"
    _REG_FOR_USER    = "button.btn-accent:nth-of-type(1)"
    _REG_FOR_MANAGER = "button.btn-accent:nth-of-type(2)"

    # ── Registration form ─────────────────────────────────────────────────
    _FIRST_NAME = "input[name='firstName'], input[name='first_name']"
    _LAST_NAME  = "input[name='lastName'],  input[name='last_name']"
    _REG_SUBMIT = "button[type='submit'].btn-accent"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def profile_link(self):
        """Возвращает локатор ссылки профиля в шапке сайта для ассертов expect()."""
        return self.page.locator(self._PROFILE_LINK)

    def open(self) -> None:
        self.navigate(URLS["home"])

    def open_login_modal(self) -> None:
        self.click_login_button()
        self.wait_visible(self._EMAIL)

    def fill_login_form(self, email: str, password: str) -> None:
        """Заполняет форму, но не отправляет её (полезно для негативных тестов)."""
        self.fill(self._EMAIL, email)
        self.fill(self._PASSWORD, password)

    def submit_login(self, force: bool = False) -> None:
        if force:
            self.page.locator(self._SUBMIT).click(force=True)
        else:
            self.click(self._SUBMIT)

    def login(self, email: str, password: str) -> None:
        self.open()
        self.open_login_modal()
        self.fill_login_form(email, password)
        self.submit_login()

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
