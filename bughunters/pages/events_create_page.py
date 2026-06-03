from __future__ import annotations
import re
from .events_page import EventsPage        # ← наследование
from bughunters.data.constants import URLS


class EventsCreatePage(EventsPage):
    """Inherits EventsPage — переиспользует click_create, EVENT_CARD и пр."""

    _TITLE        = "input[name='title'], input[placeholder*='Название']"
    _DESCRIPTION  = "textarea[name='description'], textarea[placeholder*='Описание']"
    _DATE         = "input[name='date'], input[type='date']"
    _TIME         = "input[name='time'], input[type='time']"
    _LOCATION     = "input[name='location'], input[placeholder*='Место']"
    _CAPACITY     = "input[name='capacity'], input[placeholder*='Вместимость']"
    _PUBLISH_FROM_FORM    = "button:has-text('Опубликовать')"
    _PREVIEW_FROM_FORM    = "button:has-text('Предпросмотр')"
    _SAVE = "button:has-text('Сохранить')"

    def open(self) -> "EventsCreatePage":
        self.navigate(URLS["events_create"])
        self.page.wait_for_load_state("networkidle")
        return self

    def fill_form(self, title: str, description: str = "",
                  date: str = "", time: str = "",
                  location: str = "", capacity: str = "") -> "EventsCreatePage":
        self.fill(self._TITLE, title)
        if description: self.fill(self._DESCRIPTION, description)
        if date:        self.fill(self._DATE, date)
        if time:        self.fill(self._TIME, time)
        if location:    self.fill(self._LOCATION, location)
        if capacity:    self.fill(self._CAPACITY, capacity)
        return self

    def create_event(self, title: str, description: str = "",
                     date: str = "", time: str = "",
                     location: str = "", capacity: str = "") -> "EventsCreatePage":
        self.fill_form(title=title, description=description,
                       date=date, time=time,
                       location=location, capacity=capacity)
        self.save()
        return self

    def save(self) -> None:
        self.click(self._SAVE)

    def is_saved(self) -> bool:
        return (
            self.page.get_by_role("alert", name=re.compile(r"создано|сохранено", re.IGNORECASE)).is_visible(timeout=5_000)
        )

    def publish_from_form(self) -> None:
        self.click(self._PUBLISH_FROM_FORM)

    def preview_from_form(self) -> None:
        self.click(self._PREVIEW_FROM_FORM)