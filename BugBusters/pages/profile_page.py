from BugBusters.pages.base_page import BasePage


from BugBusters.pages.base_page import BasePage


class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.first_name = page.locator('input[name="first_name"]')

        self.profile_tab = page.locator('a[href*="/ru/user/personal-information"]')
        self.purchases_tab = page.locator('a[href*="/ru/user/purchases"]')
        self.balance_tab = page.locator('a[href*="/ru/user/balance"]')

        self.company_tab = page.locator('a[href*="/ru/user/company-settings"]')
        self.events_tab = page.locator('a[href*="/ru/user/events"]')
        self.contract_data_tab = page.locator('a[href*="/ru/user/contract-data"]')
        self.contracts_tab = page.locator('a[href*="/ru/user/contracts"]')
        self.reports_tab = page.locator('a[href*="/ru/user/reports"]')
        self.qr_code_tab = page.locator('a[href*="/ru/user/qr-generator"]')
        self.withdraw_tab = page.locator('a[href*="/ru/user/withdrawal"]')
        self.publications_tab = page.locator('a[href*="/ru/user/publications"]')
        self.management_tab = page.locator('a[href*="/ru/user/management"]')

    def update_name(self, name):
        self.first_name.fill(name)
        self.page.click('button.save')

    def get_sidebar_tabs(self):
        return [
            (self.profile_tab, "/ru/user/personal-information"),
            (self.purchases_tab, "/ru/user/purchases"),
            (self.balance_tab, "/ru/user/balance"),
            (self.company_tab, "/ru/user/company-settings"),
            (self.events_tab, "/ru/user/events"),
            (self.contract_data_tab, "/ru/user/contract-data"),
            (self.contracts_tab, "/ru/user/contracts"),
            (self.reports_tab, "/ru/user/reports"),
            (self.qr_code_tab, "/ru/user/qr-generator"),
            (self.withdraw_tab, "/ru/user/withdrawal"),
            (self.publications_tab, "/ru/user/publications"),
            (self.management_tab, "/ru/user/management"),
        ]