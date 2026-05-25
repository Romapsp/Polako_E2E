from TP_Polako_E2E.base.base_page import BasePage


class TicketSelectionPage(BasePage):

    def select_free_seat(self):
        """Нажимает на плюс '+' для добавления билета."""
        self.page.get_by_role("button", name="+").click()

    def open_cart(self):
        """Открывает корзину в шапке сайта ."""
        self.page.get_by_role("button", name="Cart").click()

    def click_buy_button(self):
        """Нажимает кнопку 'Platiti' в корзине ."""
        self.page.get_by_role("button", name="Platiti").click()