from BugBusters.pages.base_page import BasePage
from playwright.sync_api import expect


class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.login_button = page.locator(
            'header button:has(use[href*="phi-caret-down-16"])'
        )
        self.email_input = page.locator('input[name="email"]')
        self.password_input = page.locator('input[name="password"]')
        self.submit_button = page.locator('button[type="submit"]')
        self.profile_link = page.locator('header a').first

    def open_login_form(self):
        self.login_button.first.click()

    def login(self, email, password):
        self.email_input.wait_for(state="visible")
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def should_have_profile_link(self):
        expect(self.profile_link).to_be_visible()