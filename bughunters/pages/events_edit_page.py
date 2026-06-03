from __future__ import annotations
from playwright.sync_api import Page
from .events_create_page import EventsCreatePage    # ← наследование
from bughunters.data.constants import BASE_URL, LANG


class EventsEditPage(EventsCreatePage):
    """Inherits EventsCreatePage — та же форма, другой URL и toast."""

    _SAVE_BTN      = "button:has-text('Сохранить')"
    _SUCCESS_TOAST = "[class*='success'], :text('обновлено'), :text('сохранено')"
    _TICKETS_BTN   = "button:has-text('Создание/редактирование билетов')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open_by_id(self, event_id: str) -> None:
        self.navigate(f"{BASE_URL}/{LANG}/user/events/{event_id}/edit")

    def update_event(self, title: str | None = None,
                     description: str | None = None) -> None:
        if title is not None:
            self.fill(self._TITLE, title)
        if description is not None:
            self.fill(self._DESCRIPTION, description)
        self.save()

    def open_tickets(self) -> None:
        self.click(self._TICKETS_BTN)