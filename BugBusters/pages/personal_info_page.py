from BugBusters.pages.base_page import BasePage

class PersonalInfoPage(BasePage):
    def update_info(self, name):
        self.page.fill("#name", name)