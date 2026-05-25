import os
from TP_Polako_E2E.base.base_page import BasePage


class PaymentGatewayPage(BasePage):
    # Локаторы формы ввода карты
    _CARD_NUMBER_INPUT = "role=textbox[name='BROJ KARTICE (bez razmaka):']"
    _EXPIRY_MONTH_SELECT = "id=Ecom_Payment_Card_ExpDate_Month"  # Используем ID или label
    _EXPIRY_YEAR_SELECT = "id=Ecom_Payment_Card_ExpDate_Year"  # Обычно на шлюзах два селекта
    _CVV_INPUT = "role=textbox[name='CVC2/ CVV2 kod:']"
    _SUBMIT_PAYMENT_BUTTON = "role=button[name='Plati']"  # Или то имя, которое у кнопки на сербском/английском

    # Локаторы симулятора банка (кнопки успешных/неуспешных сценариев)
    # ПРИМЕЧАНИЕ: Тексты кнопок ниже ориентировочные. Мы обновим их, как только ты пришлешь точный codegen.
    _APPROVE_BUTTON = "role=button[name=/Approve|Potvrdi|Oдобри/i]"
    _DECLINE_BUTTON = "role=button[name=/Decline|Odbij|Otkáži/i]"
    _INSUFFICIENT_FUNDS_BUTTON = "role=button[name=/Insufficient|Nema sredstava/i]"

    def fill_card_details(self, card_number: str, expiry_month: str, expiry_year: str, cvv: str):
        """Заполняет данные пластиковой карты из .env на платежном шлюзе."""
        self.page.locator(self._CARD_NUMBER_INPUT).wait_for(state="visible", timeout=15000)

        self.fill(self._CARD_NUMBER_INPUT, card_number)

        # Playwright умеет выбирать элементы в выпадающих списках через select_option
        self.page.locator(self._EXPIRY_MONTH_SELECT).select_option(expiry_month)
        self.page.locator(self._EXPIRY_YEAR_SELECT).select_option(expiry_year)

        self.fill(self._CVV_INPUT, cvv)

    def click_submit_payment(self):
        """Нажимает кнопку совершения платежа на форме ввода карты."""
        self.click(self._SUBMIT_PAYMENT_BUTTON)

    def simulate_successful_payment(self):
        """Симулирует успешный ответ банка (нажатие кнопки Одобрить транзакцию)."""
        self.page.locator(self._APPROVE_BUTTON).wait_for(state="visible", timeout=10000)
        self.click(self._APPROVE_BUTTON)

    def simulate_declined_payment(self):
        """Симулирует отказ банка (нажатие кнопки Отклонить транзакцию)."""
        self.page.locator(self._DECLINE_BUTTON).wait_for(state="visible", timeout=10000)
        self.click(self._DECLINE_BUTTON)

    def simulate_insufficient_funds(self):
        """Симулирует ошибку нехватки средств."""
        self.page.locator(self._INSUFFICIENT_FUNDS_BUTTON).wait_for(state="visible", timeout=10000)
        self.click(self._INSUFFICIENT_FUNDS_BUTTON)