from __future__ import annotations
from .events_create_page import EventsCreatePage
from bughunters.data.constants import BASE_URL, LANG


class EventsEditPage(EventsCreatePage):
    _TICKETS_BTN = "button:has-text('Создание/редактирование билетов')"

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
