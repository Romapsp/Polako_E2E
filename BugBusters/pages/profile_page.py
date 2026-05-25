from BugBusters.pages.base_page import BasePage

class ProfilePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name = page.locator('input[name="first_name"]')
        self.purchases_tab = page.locator('text=Purchases')

    def update_name(self, name):
        self.first_name.fill(name)
        self.page.click('button.save')