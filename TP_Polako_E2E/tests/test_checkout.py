import pytest
import os
from TP_Polako_E2E.base.base_test import BaseTest
from TP_Polako_E2E.pages.ticket.ticket_selection_page import TicketSelectionPage
from TP_Polako_E2E.pages.ticket.checkout_page import CheckoutPage


class TestTicketPurchase(BaseTest):

    @pytest.mark.ui
    @pytest.mark.smoke
    def test_successful_ticket_checkout_flow(self):
        self.login_page.login_as_valid_user()
        ticket_selection = TicketSelectionPage(self.page)
        checkout = CheckoutPage(self.page)

        test_event_url = "https://stg-client.polakohedonist.club/sr/events/ezhegodnyj-rok-koncert-uchenikov-muzykalnoj-shkoly-kreativni-m-kutak-ezhegodnyj-rok-koncer-test-location-ns-2026-05-27-12-00-1"
        self.page.goto(test_event_url)

        ticket_selection.select_free_seat()
        ticket_selection.open_cart()
        ticket_selection.click_buy_button()

        test_email = os.getenv("VALID_EMAIL", "master4610@gmail.com")
        checkout.fill_checkout_form(
            first_name="master",
            last_name="kr",
            email=test_email
        )

        checkout.accept_terms_and_conditions()
        checkout.click_pay_button()
        checkout.proceed_to_payment_gateway()

        card_number = os.getenv("CARD_NUMBER", "4111111111111111")
        card_month = os.getenv("CARD_MONTH", "12")
        card_year = os.getenv("CARD_YEAR", "27")
        card_cvv = os.getenv("CARD_CVV", "123")

        print(
            f"\n[ENV] Данные для ввода на шлюзе: Номер: {card_number}, Срок: {card_month}/{card_year}, CVV: {card_cvv}")

        self.page.pause()