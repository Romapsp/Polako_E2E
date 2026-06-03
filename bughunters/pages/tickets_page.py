from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage


class TicketsPage(BasePage):
    """Wizard создания билетов: тип → категории → сохранение."""

    _TYPE_NO_SEATS    = "button:has-text('Без мест')"
    _TYPE_WITH_SEATS  = "button:has-text('С местами')"
    _CONTINUE_BTN     = "button:has-text('Продолжить')"
    _TICKET_NAME      = "input[name='ticketName'], input[placeholder*='Название']"
    _QUANTITY         = "input[name='quantity'], input[placeholder*='Количество']"
    _PRICE            = "input[name='price'], input[placeholder*='Цена']"
    _SAVE_TICKET_BTN  = "button:has-text('Сохранить')"
    _CREATE_TICKETS   = "button:has-text('Создать билеты')"
    _SUCCESS          = "[class*='success'], :text('билеты созданы')"
    _ERROR            = "[class*='error'], .toast-error"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def select_no_seats(self) -> None:
        self.click(self._TYPE_NO_SEATS)
        self.click(self._CONTINUE_BTN)

    def select_with_seats(self, hall_name: str = "") -> None:
        self.click(self._TYPE_WITH_SEATS)
        if hall_name:
            self.page.locator(f":text('{hall_name}')").click()
        self.click(self._CONTINUE_BTN)

    def fill_ticket_category(self, name: str, quantity: str, price: str) -> None:
        self.fill(self._TICKET_NAME, name)
        self.fill(self._QUANTITY, quantity)
        self.fill(self._PRICE, price)
        self.click(self._SAVE_TICKET_BTN)

    def create_tickets(self) -> None:
        self.click(self._CREATE_TICKETS)

    def is_created(self) -> bool:
        return self.page.locator(self._SUCCESS).is_visible(timeout=5_000)

    def get_validation_error(self) -> str:
        loc = self.page.locator(self._ERROR)
        return loc.inner_text() if loc.is_visible() else ""