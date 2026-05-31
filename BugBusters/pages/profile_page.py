from BugBusters.pages.base_page import BasePage


from BugBusters.pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.first_name = page.locator('input[name="first_name"]')

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
        self.page.click('button.save')

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

    def close_whats_new_popup(self):
        close_button = self.page.get_by_role("button", name="Close")

        if close_button.is_visible():
            close_button.click()