from .auth_page import AuthPage
from .personal_info_page import PersonalInfoPage
from .purchases_page import PurchasesPage
from .events_page import EventsPage
from .events_create_page import EventsCreatePage
from .events_edit_page import EventsEditPage
from .tickets_page import TicketsPage


class Pages:
    """Фасад — один импорт даёт доступ ко всем page objects."""

    def __init__(self, page) -> None:
        self.auth          = AuthPage(page)
        self.personal_info = PersonalInfoPage(page)
        self.purchases     = PurchasesPage(page)
        self.events        = EventsPage(page)
        self.events_create = EventsCreatePage(page)
        self.events_edit   = EventsEditPage(page)
        self.tickets       = TicketsPage(page)


__all__ = [
    "Pages", "AuthPage", "PersonalInfoPage", "PurchasesPage",
    "EventsPage", "EventsCreatePage", "EventsEditPage", "TicketsPage",
]