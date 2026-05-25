from BugBusters.pages.base_page import BasePage

class PurchasePage(BasePage):
    def get_history(self):
        return self.page.locator(".purchase-item")