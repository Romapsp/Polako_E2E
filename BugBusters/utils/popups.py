from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError


def close_whats_new_popup(page: Page):
    try:
        page.get_by_role("button", name="Close").click(timeout=3000)
    except PlaywrightTimeoutError:
        pass