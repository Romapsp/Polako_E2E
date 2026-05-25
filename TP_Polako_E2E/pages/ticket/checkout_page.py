from TP_Polako_E2E.base.base_page import BasePage

class CheckoutPage(BasePage):
    _FIRST_NAME_INPUT = "input[name='customer_first_name']"
    _LAST_NAME_INPUT = "input[name='customer_second_name']"
    _EMAIL_INPUT = "input[name='customer_email']"
    _CONFIRM_EMAIL_INPUT = "input[name='customer_email_repeat']"
    _TERMS_CHECKBOX_1 = ".mt-5 > .flex.flex-col.gap-1 > .relative > .min-w-4"
    _TERMS_CHECKBOX_2 = ".flex.h-5"

    def fill_checkout_form(self, first_name: str, last_name: str, email: str):
        self.page.locator(self._FIRST_NAME_INPUT).wait_for(state="visible", timeout=10000)
        self.fill(self._FIRST_NAME_INPUT, first_name)
        self.fill(self._LAST_NAME_INPUT, last_name)
        self.fill(self._EMAIL_INPUT, email)
        self.fill(self._CONFIRM_EMAIL_INPUT, email)

    def accept_terms_and_conditions(self):
        self.click(self._TERMS_CHECKBOX_1)
        self.page.locator(self._TERMS_CHECKBOX_2).first.click()

    def click_pay_button(self):
        self.page.get_by_role("button", name="Plati — 2020 RSD").click()

    def proceed_to_payment_gateway(self):
        self.page.get_by_role("link", name="na link").click()