from __future__ import annotations
from playwright.sync_api import Page
from .base_page import BasePage
from bughunters.data.constants import URLS


class PurchasesPage(BasePage):
    _PAGE_HEADING = "h1, h2"
    _NAV_LINK = "a[href*='/user/purchases']"

    # CSR loading indicator
    _SPINNER = "div.animate-spin"

    # Purchase items
    _PURCHASE_ITEM = (
        "main li, main article, "
        "[class*='purchase'], [class*='order'], "
        "[class*='ticket'], [class*='booking']"
    )

    # Empty-state: text-based selectors that survive CSS class changes
    _EMPTY_STATE_TEXTS = [
        "Покупок пока нет",
        "нет покупок",
        "пусто",
        "No purchases",
        "История пуста",
    ]

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def open(self) -> None:
        self.navigate(URLS["purchases"])
        self._wait_for_csr()

    def _wait_for_csr(self) -> None:
        """Wait for React CSR hydration to finish (spinner disappears)."""
        spinner = self.page.locator(self._SPINNER)
        try:
            spinner.first.wait_for(state="visible", timeout=3_000)
            spinner.first.wait_for(state="hidden", timeout=15_000)
        except Exception:
            pass  # Spinner already gone or never appeared — content is ready

    def get_purchase_count(self) -> int:
        return self.page.locator(self._PURCHASE_ITEM).count()

    def is_empty(self) -> bool:
        """Return True if the page renders any known empty-state indicator."""
        for text in self._EMPTY_STATE_TEXTS:
            try:
                loc = self.page.get_by_text(text, exact=False)
                if loc.first.is_visible(timeout=3_000):
                    return True
            except Exception:
                continue
        # Fallback: a container with class containing 'empty'
        try:
            if self.page.locator("[class*='empty']").first.is_visible(timeout=2_000):
                return True
        except Exception:
            pass
        return False
