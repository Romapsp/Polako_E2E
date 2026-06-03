from __future__ import annotations
from playwright.sync_api import expect
import re
from .base_page import BasePage
from bughunters.data.constants import URLS


class PersonalInfoPage(BasePage):
    # ── Form fields ───────────────────────────────────────────────────────
    _FIRST_NAME       = "input[name='first_name']"
    _LAST_NAME        = "input[name='last_name']"
    _EMAIL            = "input[name='email']"
    _PHONE            = "input[name='phone']"
    _INSTAGRAM        = "input[name='instagram']"
    _TELEGRAM         = "input[name='telegram']"
    _NEW_PASSWORD     = "input[name='new_password']"
    _CONFIRM_PASSWORD = "input[name='confirm_password']"

    # ── Buttons ───────────────────────────────────────────────────────────
    # Two submit buttons: first = save profile, last = change password
    _SAVE_BTN         = "button[type='submit'][data-slot='button']"
    _CHANGE_PWD_BTN   = "button[type='submit'][data-slot='button']"
    # Logout: unique — type=button, accent background, confirmed single element
    _LOGOUT_BTN       = "button[type='button'][class*='bg-accent']"

    # ── Sidebar navigation ────────────────────────────────────────────────
    _NAV_PERSONAL_INFO = "a[href*='/user/personal-information']"
    _NAV_PURCHASES     = "a[href*='/user/purchases']"

    # ── "What's new" modal (appears after first login) ───────────────────
    _MODAL_OVERLAY    = "div.fixed.inset-0.z-50"
    _MODAL_CLOSE_BTN  = "div[role='dialog'] button[type='button'][class*='border-gray-200']"

    def open(self) -> None:
        self.navigate(URLS["personal_info"])
        self._dismiss_modal_if_present()

    def _dismiss_modal_if_present(self) -> None:
        """Dismiss the 'What's new' announcement modal if it blocks the page."""
        overlay = self.page.locator(self._MODAL_OVERLAY)
        try:
            overlay.wait_for(state="visible", timeout=3_000)
        except Exception:
            return  # no modal — nothing to do
        try:
            self.page.locator(self._MODAL_CLOSE_BTN).click(timeout=3_000)
            overlay.wait_for(state="hidden", timeout=5_000)
        except Exception:
            self.page.keyboard.press("Escape")
            try:
                overlay.wait_for(state="hidden", timeout=3_000)
            except Exception:
                pass

    def get_first_name(self) -> str:
        self._dismiss_modal_if_present()
        return self.page.locator(self._FIRST_NAME).input_value()

    def get_email(self) -> str:
        self._dismiss_modal_if_present()
        return self.page.locator(self._EMAIL).input_value()

    def update_profile(self, first_name: str = None, last_name: str = None,
                       phone: str = None, instagram: str = None, telegram: str = None) -> None:
        self._dismiss_modal_if_present()
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
        self.page.locator(self._SAVE_BTN).first.click()

    def navigate_to_purchases(self) -> None:
        """Navigate to purchases using goto — clicking sidebar link exits auth context."""
        self.navigate(URLS["purchases"])
        self._dismiss_modal_if_present()

    def navigate_to_personal_info(self) -> None:
        """Navigate back to personal-info using goto."""
        self.navigate(URLS["personal_info"])
        self._dismiss_modal_if_present()

    def click_logout(self) -> None:
        self._dismiss_modal_if_present()
        self.page.locator(self._LOGOUT_BTN).click()

    # ── Verify helpers ────────────────────────────────────────────────────

    def verify_profile_fields_visible(self) -> None:
        self._dismiss_modal_if_present()
        for name in ("first_name", "last_name", "email", "phone", "instagram", "telegram"):
            expect(self.page.locator(f"input[name='{name}']")).to_be_visible()

    def verify_password_fields_visible(self) -> None:
        self._dismiss_modal_if_present()
        expect(self.page.locator(self._NEW_PASSWORD)).to_be_visible()
        expect(self.page.locator(self._CONFIRM_PASSWORD)).to_be_visible()

    def verify_sidebar_links_visible(self) -> None:
        self._dismiss_modal_if_present()
        expect(self.page.locator(self._NAV_PERSONAL_INFO).first).to_be_visible()
        expect(self.page.locator(self._NAV_PURCHASES).first).to_be_visible()

    def verify_logout_btn_visible(self) -> None:
        self._dismiss_modal_if_present()
        expect(self.page.locator(self._LOGOUT_BTN)).to_be_visible()

    def verify_save_succeeded(self, timeout: int = 5_000) -> None:
        """
        Verify profile was saved by checking the page doesn't show an error
        and the save button is still present (page wasn't redirected away).
        The app has no toast — success is implicit when no error appears.
        """
        self._dismiss_modal_if_present()
        # Confirm we're still on the personal-info page (not redirected on error)
        expect(self.page).to_have_url(
            re.compile(r"user/personal-information"), timeout=timeout
        )
        # Confirm no error element is visible
        error_loc = self.page.locator("[role='alert'][class*='error'], [class*='error-message']")
        assert not error_loc.is_visible(timeout=2_000), \
            "An error message appeared after saving the profile"

    def change_password(self, new_password: str) -> None:
        self._dismiss_modal_if_present()
        self.fill(self._NEW_PASSWORD, new_password)
        self.fill(self._CONFIRM_PASSWORD, new_password)
        self.page.locator(self._CHANGE_PWD_BTN).last.click()
