from __future__ import annotations
import time
from playwright.sync_api import Page, Locator


def wait_for_url_part(page: Page, fragment: str, timeout: int = 15_000) -> None:
    page.wait_for_url(f"**{fragment}**", timeout=timeout)


def fill_field(page: Page, selector: str, value: str) -> None:
    loc = page.locator(selector)
    loc.wait_for(state="visible")
    loc.clear()
    loc.fill(value)


def click_element(page: Page, selector: str) -> None:
    loc = page.locator(selector)
    loc.wait_for(state="visible")
    loc.click()


def get_text(page: Page, selector: str) -> str:
    return page.locator(selector).inner_text()


def is_visible(page: Page, selector: str) -> bool:
    return page.locator(selector).is_visible()


def take_screenshot(page: Page, name: str, folder: str = "screenshots") -> None:
    import os
    os.makedirs(folder, exist_ok=True)
    page.screenshot(path=f"{folder}/{name}_{int(time.time())}.png", full_page=True)