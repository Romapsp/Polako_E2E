from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from bughunters.data.constants import TIMEOUTS


class BasePage:
    # Overlay selector: the "What's new" announcement modal
    _MODAL_OVERLAY = "div[role='dialog'][aria-modal='true'], div.fixed.inset-0.z-50"
    # The close button inside the modal (text "Закрыть" or any button inside the overlay)
    _MODAL_CLOSE_BTN = "div[role='dialog'][aria-modal='true'] button[type='button']"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._timeout = TIMEOUTS["element"]
        self._header_user_link = "a[href*='/user']"
        self._header_login_btn = "button.ml-4"

    def navigate(self, url: str) -> None:
        self.page.goto(url, timeout=TIMEOUTS["navigation"])

    @property
    def current_url(self) -> str:
        return self.page.url

    def locator(self, selector: str) -> Locator:
        return self.page.locator(selector)

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        loc = self.page.locator(selector)
        loc.clear()
        loc.fill(value)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_visible(self, selector: str, timeout: int | None = None) -> Locator:
        loc = self.page.locator(selector)
        loc.wait_for(state="visible", timeout=timeout or self._timeout)
        return loc

    def expect_url_contains(self, fragment: str) -> None:
        expect(self.page).to_have_url(f"**{fragment}**")

    # ── Modal helper ──────────────────────────────────────────────────────────

    def close_modal_if_present(self, timeout: int = 3_000) -> None:
        """Dismiss the announcement/whats-new modal if it is blocking the page.

        Strategy (in order):
          1. Click the "Закрыть" / "Close" button inside the overlay.
          2. Fall back to pressing Escape.
        Silently ignored when no modal is present.
        """
        try:
            overlay = self.page.locator(self._MODAL_OVERLAY).first
            overlay.wait_for(state="visible", timeout=timeout)
        except Exception:
            return  # No modal — nothing to do

        try:
            close_btn = self.page.locator(self._MODAL_CLOSE_BTN).first
            close_btn.wait_for(state="visible", timeout=2_000)
            close_btn.click()
        except Exception:
            # Button not found or not clickable — try Escape
            self.page.keyboard.press("Escape")

        # Wait until overlay is gone so subsequent actions are not blocked
        try:
            self.page.locator(self._MODAL_OVERLAY).first.wait_for(
                state="hidden", timeout=5_000
            )
        except Exception:
            pass  # If it doesn't disappear, the test will fail with a clear message

    # ── Header helpers ────────────────────────────────────────────────────────

    def click_login_button(self) -> None:
        self.page.locator(self._header_login_btn).first.click()

    def click_profile_button(self) -> None:
        self.page.locator(self._header_user_link).first.click()

    def is_logged_in(self, timeout: int = 10_000) -> bool:
        try:
            self.page.locator(self._header_user_link).first.wait_for(
                state="visible", timeout=timeout
            )
            return True
        except Exception:
            return False

    def logout(self) -> None:
        self.click_profile_button()
        logout_btn = self.page.locator("button[type='button'][class*='group/button']")
        logout_btn.click()
