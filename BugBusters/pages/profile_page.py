from BugBusters.pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.first_name = page.locator('input[name="first_name"]')
        self.last_name = page.locator('input[name="last_name"]')
        self.email = page.locator('input[name="email"]')
        self.phone = page.locator('input[name="phone"]')

        self.instagram = page.locator('input[name="instagram"]')

        self.telegram = page.locator('input[name="telegram"]')

        self.new_password = page.locator('input[name="new_password"]')
        self.confirm_password = page.locator('input[name="confirm_password"]')

        self.save_button = page.get_by_role("button", name="Save")

        self.profile_tab = page.locator('a[href*="/user/personal-information"]')
        self.purchases_tab = page.locator('a[href*="/user/purchases"]')
        self.balance_tab = page.locator('a[href*="/user/balance"]')

        self.company_tab = page.locator('a[href*="/user/company-settings"]')
        self.events_tab = page.locator('a[href*="/user/events"]')
        self.contract_data_tab = page.locator('a[href*="/user/contract-data"]')
        self.contracts_tab = page.locator('a[href*="/user/contracts"]')
        self.reports_tab = page.locator('a[href*="/user/reports"]')
        self.qr_code_tab = page.locator('a[href*="/user/qr-generator"]')
        self.withdraw_tab = page.locator('a[href*="/user/withdrawal"]')
        self.publications_tab = page.locator('a[href*="/user/publications"]')
        self.management_tab = page.locator('a[href*="/user/management"]')

    def update_name(self, name):
        self.first_name.fill(name)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_first_name_value(self):
        return self.first_name.input_value()

    def update_last_name(self, last_name):
        self.last_name.fill(last_name)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")


    def get_last_name_value(self):
        return self.last_name.input_value()

    def update_email(self, email):
        self.email.fill(email)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_email_value(self):
        return self.email.input_value()

    def update_phone(self, phone):
        self.phone.fill(phone)
        self.save_button.click()

        from playwright.sync_api import expect
        expect(self.page.locator("text='Profile updated'")).to_be_visible()



    def get_phone_value(self):
        return self.phone.input_value()

    def update_instagram(self, instagram):
        self.instagram.fill(instagram)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_instagram_value(self):
        return self.instagram.input_value()

    def update_telegram(self, telegram):
        self.telegram.fill(telegram)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_telegram_value(self):
        return self.telegram.input_value()

    def update_password(self, new_password, confirm_password):
        self.new_password.fill(new_password)
        self.confirm_password.fill(confirm_password)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_sidebar_tabs(self):
        return [
            (self.profile_tab, "/en/user/personal-information"),
            (self.purchases_tab, "/en/user/purchases"),
            (self.balance_tab, "/en/user/balance"),
            (self.company_tab, "/en/user/company-settings"),
            (self.events_tab, "/en/user/events"),
            (self.contract_data_tab, "/en/user/contract-data"),
            (self.contracts_tab, "/en/user/contracts"),
            (self.reports_tab, "/en/user/reports"),
            (self.qr_code_tab, "/en/user/qr-generator"),
            (self.withdraw_tab, "/en/user/withdrawal"),
            (self.publications_tab, "/en/user/publications"),
            (self.management_tab, "/en/user/management"),
        ]

    def save_profile(self):
        with self.page.expect_response(
                lambda r: (
                        r.url.endswith("/api/users/me")
                        and r.request.method == "PATCH"
                ),
                timeout=10000
        ) as response_info:
            self.save_button.click()

        response = response_info.value

        assert response.ok, f"Failed to save profile: {response.status} {response.text()}"
