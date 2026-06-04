from __future__ import annotations
from .base_page import BasePage
from bughunters.data.constants import URLS


class EventsPage(BasePage):
    _EVENT_CARD    = "[class*='event-card'], [class*='eventCard']"
    _PUBLISH_BTN   = "button:has-text('Опубликовать')"
    _DRAFT_BTN     = "button:has-text('В черновик')"
    _PREVIEW_BTN   = "button:has-text('Предпросмотр')"
    _EDIT_BTN      = "button:has-text('Редактировать')"
    _COPY_LINK_BTN = "button:has-text('Скопировать ссылку')"
    _EMPTY_STATE_CLASS = "[class*='empty']"

    def _get_card(self, card_index: int):
        loc = self.page.locator(self._EVENT_CARD).nth(card_index)
        loc.wait_for(state="visible", timeout=self._timeout)
        return loc

    def open(self) -> None:
        self.navigate(URLS["events_list"])
        self.page.locator(self._EVENT_CARD + ", " + self._EMPTY_STATE_CLASS).first.wait_for(
            state="visible", timeout=self._timeout,
        )

    def click_create(self) -> None:
        self.page.get_by_role("button", name="Создать мероприятие").or_(
            self.page.get_by_role("link", name="Создать мероприятие")
        ).click()

    def click_edit_for_card(self, card_index: int = 0) -> None:
        self._get_card(card_index).locator(self._EDIT_BTN).click()

    def click_publish_for_card(self, card_index: int = 0) -> None:
        self._get_card(card_index).locator(self._PUBLISH_BTN).click()

    def click_draft_for_card(self, card_index: int = 0) -> None:
        self._get_card(card_index).locator(self._DRAFT_BTN).click()

    def click_preview_for_card(self, card_index: int = 0) -> None:
        self._get_card(card_index).locator(self._PREVIEW_BTN).click()

    def click_copy_link_for_card(self, card_index: int = 0) -> None:
        self._get_card(card_index).locator(self._COPY_LINK_BTN).click()

    def go_back_from_preview(self) -> None:
        self.page.get_by_role("link", name="Назад к мероприятиям").or_(
            self.page.get_by_role("button", name="Назад")
        ).click()

    def get_event_count(self) -> int:
        return self.page.locator(self._EVENT_CARD).count()

    def is_empty(self) -> bool:
        return (
            self.page.locator(self._EMPTY_STATE_CLASS).is_visible()
            or self.page.get_by_text("нет мероприятий").is_visible()
        )
