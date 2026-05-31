from BugBusters.pages.base_page import BasePage
from playwright.sync_api import expect


class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.login_btn = page.locator(
            'header button:has(use[href*="phi-caret-down-16"])'
        )

        self.no_account_link = page.locator(
            'button.text-center.text-sm.text-black.underline.underline-offset-2'
        )

        self.email_input = page.locator(
            'form input[name="email"]'
        )

        self.password_input = page.locator(
            'form input[name="password"]'
        )

        self.name_input = page.locator(
            'form input[name="first_name"]'
        )

        self.submit_button = page.locator(
            'form button[type="submit"]'
        )


        self.avatar_circle = page.locator(
            'header span.text.m-auto.text-white'
        )
        self.multilang_error_message = page.locator('.bg-fault + p'
        )

        self.error_popup_title = page.locator('div.absolute.right-0 > p.text-2xl'
        )

    def navigate_to_registration(self):
        self.login_btn.first.wait_for(state="visible", timeout=5000)
        self.login_btn.first.click()

        self.no_account_link.wait_for(state="visible", timeout=5000)
        self.no_account_link.click()

    def fill_registration_form(self, name, email, password):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)

    def submit_registration(self):
        self.submit_button.wait_for(state="visible", timeout=5000)
        self.submit_button.click()

    def register(self, name, email, password):
        self.fill_registration_form(name, email, password)
        self.submit_registration()

    def should_have_avatar_circle(self, user_name=""):
        expect(self.avatar_circle).to_be_visible(timeout=5000)

        if user_name:
            first_letter = user_name[0].upper()
            expect(self.avatar_circle).to_have_text(first_letter)
        else:
            expect(self.avatar_circle).not_to_be_empty()

    def should_have_registration_error(self):
        expect(self.error_popup_title).to_be_visible(timeout=5000)
        expect(self.error_popup_title).not_to_be_empty()

        expect(self.multilang_error_message).to_be_visible(timeout=5000)
        expect(self.multilang_error_message).not_to_be_empty()