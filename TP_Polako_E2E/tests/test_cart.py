import pytest

from TP_Polako_E2E.base.base_test import BaseTest


class TestTicketCart(BaseTest):

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_add_first_ticket_to_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.open_cart()
        self.ticket_selection_page.assert_cart_timer_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_add_second_ticket_to_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("second")
        self.ticket_selection_page.open_cart()
        self.ticket_selection_page.assert_cart_timer_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_add_third_ticket_to_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("third")
        self.ticket_selection_page.open_cart()
        self.ticket_selection_page.assert_cart_timer_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_cart_badge_visible_on_add(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")

        self.cart_page.verify_cart_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_remove_first_ticket_from_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()
        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_remove_second_ticket_from_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("second")
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()
        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_remove_third_ticket_from_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("third")
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()
        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    @pytest.mark.parametrize("ticket_type", ["first", "second", "third"])
    def test_remove_ticket_from_cart(self, ticket_type):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket(ticket_type)
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()
        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_add_multiple_tickets_to_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.select_ticket("second")
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_remove_one_ticket_from_multiple_tickets(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.select_ticket("second")
        self.ticket_selection_page.open_cart()

        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_visible()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_clear_all_tickets_from_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.select_ticket("second")
        self.ticket_selection_page.select_ticket("third")

        self.ticket_selection_page.open_cart()

        self.cart_page.clear_all_tickets()

        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_cart_badge_disappears_after_removal(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")

        self.cart_page.verify_cart_is_visible()

        self.ticket_selection_page.open_cart()

        self.cart_page.remove_ticket()
        self.cart_page.verify_cart_is_empty()

    @pytest.mark.skip(reason="UI changed: cart flow temporarily redesigned")
    def test_ticket_remains_after_reopening_cart(self):
        self.login_page.login_as_valid_user()

        self.events_list_page.click_active_slider_event()

        self.ticket_selection_page.select_ticket("first")
        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()

        self.ticket_selection_page.open_cart()

        self.cart_page.verify_cart_is_visible()