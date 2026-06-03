from BugBusters.pages.base_page import BasePage


# OopCompanion:suppressRename


class EventBasePage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.title_field = page.locator('input[name="title"]')
        self.desc_field = page.locator('textarea[name="description"]')

class EventCreatePage(EventBasePage):
    def create(self, title, desc):
        self.title_field.fill(title)
        self.desc_field.fill(desc)
        self.page.click('#btn-create')

class EventEditPage(EventBasePage):
    def edit(self, new_title):
        self.title_field.clear()
        self.title_field.fill(new_title)
        self.page.click('#btn-update')