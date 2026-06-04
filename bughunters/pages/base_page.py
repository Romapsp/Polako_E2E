from __future__ import annotations
from playwright.sync_api import Page, Locator, expect
from bughunters.data.constants import TIMEOUTS


class BasePage:
    _MODAL_OVERLAY   = "div[role='dialog'][aria-modal='true'], div.fixed.inset-0.z-50"
    _MODAL_CLOSE_BTN = "div[role='dialog'][aria-modal='true'] button[type='button']"

    _HEADER_USER_LINK = "a[href*='/user']"
    _HEADER_LOGIN_BTN = "button.ml-4"

    def __init__(self, page: Page) -> None:
        self.page = page
        self._timeout = TIMEOUTS["element"]

    # ── Navigation ──────────────────────────────────────────────────────────

    def navigate(self, url: str) -> None:
        self.page.goto(url, timeout=TIMEOUTS["navigation"])

    def goto_with_retry(
        self, url: str, expected_substring: str,
        retries: int = 1, wait_timeout: int = 30_000,
        stable_ms: int = 800,
    ) -> None:
        """Navigate and retry once if the app redirected us away (CI flakiness).
        After the substring check, waits ``stable_ms`` to detect CSR redirects
        triggered after the initial page load (Next.js auth-guard pattern).
        Raises AssertionError if the final URL does not contain the expected fragment.
        """
        for attempt in range(retries + 1):
            self.page.goto(url, timeout=TIMEOUTS["navigation"])
            self.page.wait_for_load_state("domcontentloaded", timeout=wait_timeout)
            if expected_substring in self.page.url:
                self.page.wait_for_timeout(stable_ms)
                if expected_substring in self.page.url:
                    return
            if attempt < retries:
                self.page.wait_for_timeout(2_000)
        raise AssertionError(
            f"After {retries + 1} attempt(s) URL {self.page.url!r} "
            f"does not contain {expected_substring!r}"
        )

    @property
    def current_url(self) -> str:
        return self.page.url

    def current_url_matches(
        self, pattern, timeout: int | None = None,
    ) -> bool:
        """Auto-retrying check: current URL matches the pattern within ``timeout``."""
        try:
            expect(self.page).to_have_url(pattern, timeout=timeout or self._timeout)
            return True
        except Exception:
            return False

    # ── Low-level helpers (intended for use by page objects) ────────────────

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

    # ── Header ──────────────────────────────────────────────────────────────

    def _click_login_button(self) -> None:
        self.page.locator(self._HEADER_LOGIN_BTN).first.click()

    # ── Modal ───────────────────────────────────────────────────────────────

    def close_modal_if_present(self, timeout: int = 3_000) -> None:
        """Dismiss the announcement/whats-new modal if it is blocking the page.
        Tries the close button, then falls back to Escape. Silently ignored
        when no modal is present.
        """
        try:
            self.page.locator(self._MODAL_OVERLAY).first.wait_for(
                state="visible", timeout=timeout,
            )
        except Exception:
            return

        try:
            close_btn = self.page.locator(self._MODAL_CLOSE_BTN).first
            close_btn.wait_for(state="visible", timeout=2_000)
            close_btn.click()
        except Exception:
            self.page.keyboard.press("Escape")

        try:
            self.page.locator(self._MODAL_OVERLAY).first.wait_for(
                state="hidden", timeout=5_000,
            )
        except Exception:
            pass

    # ── Auth state ──────────────────────────────────────────────────────────

    def is_logged_in(self, timeout: int = 10_000) -> bool:
        try:
            self.page.locator(self._HEADER_USER_LINK).first.wait_for(
                state="visible", timeout=timeout,
            )
            return True
        except Exception:
            return False

    def wait_until_logged_out(self, timeout: int = 5_000) -> None:
        """Auto-retrying assertion: the profile link is not visible for the
        whole window. Use after logout / session expiry."""
        expect(self.page.locator(self._HEADER_USER_LINK).first).not_to_be_visible(
            timeout=timeout,
        )
