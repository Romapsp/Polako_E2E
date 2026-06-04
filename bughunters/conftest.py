import json
import os
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from bughunters.data.constants import MANAGER_USER, TIMEOUTS, URLS
from bughunters.pages import Pages
from bughunters.pages.base_page import BasePage

API_LOGIN_URL = "https://stg.polakohedonist.club/api/auth/login"


# ── Browser (session-scoped) ──────────────────────────────────────────────────

@pytest.fixture(scope="session")
def browser_instance():
    with sync_playwright() as pw:
        headless = os.environ.get("CI", "false").lower() == "true"
        browser = pw.chromium.launch(headless=headless)
        yield browser


# ── Unauthenticated fixtures ──────────────────────────────────────────────────

@pytest.fixture(scope="function")
def context(browser_instance: Browser) -> BrowserContext:
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    yield ctx
    ctx.close()


@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Page:
    p = context.new_page()
    yield p
    p.close()


# ── Auth helpers ──────────────────────────────────────────────────────────────
# Primary auth = API cookie injection (fast). Fallback = full UI login (slower
# but sets every Next.js hydration token; use when CSR navigation between
# /user/* pages breaks with API auth).

def _api_login(browser: Browser):
    ctx = browser.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    page = ctx.new_page()

    resp = page.request.post(
        API_LOGIN_URL,
        data=json.dumps({
            "email":    MANAGER_USER["email"],
            "password": MANAGER_USER["password"],
        }),
        headers={"Content-Type": "application/json"},
    )
    assert resp.ok, f"API login failed: {resp.status} {resp.text()}"
    access_token = resp.json()["data"]["access_token"]

    # Visit stg.* first so the cookie domain is registered in the browser context
    page.goto(URLS["personal_info"], timeout=TIMEOUTS["navigation"])
    ctx.add_cookies([{
        "name":     "access_token",
        "value":    access_token,
        "domain":   "stg.polakohedonist.club",
        "path":     "/",
        "httpOnly": False,
        "secure":   True,
        "sameSite": "Lax",
    }])
    page.reload(timeout=TIMEOUTS["navigation"])
    page.locator("input[name='first_name']").wait_for(
        state="visible", timeout=TIMEOUTS["navigation"]
    )
    BasePage(page).close_modal_if_present()
    return page, ctx


def _ui_login(page: Page) -> None:
    page.goto(URLS["home"], timeout=TIMEOUTS["navigation"])
    page.locator("button.ml-4").click()
    page.locator("input[name='email']").fill(MANAGER_USER["email"])
    page.locator("input[name='password']").fill(MANAGER_USER["password"])
    page.locator("button[type='submit'].btn-accent").click()
    page.locator("a[href*='/user']").first.wait_for(
        state="visible", timeout=TIMEOUTS["navigation"]
    )
    page.goto(URLS["personal_info"], timeout=TIMEOUTS["navigation"])
    BasePage(page).close_modal_if_present()


# ── Authenticated fixtures ────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def authenticated_page(browser_instance: Browser) -> Page:
    """Primary fixture — API login (fast)."""
    page, ctx = _api_login(browser_instance)
    yield page
    ctx.close()


@pytest.fixture(scope="function")
def authenticated_page_ui(browser_instance: Browser) -> Page:
    """Fallback fixture — full UI login. Use when API auth breaks CSR nav."""
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    p = ctx.new_page()
    _ui_login(p)
    yield p
    ctx.close()


# ── Page-object facades ───────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def pages(page: Page) -> Pages:
    return Pages(page)


@pytest.fixture(scope="function")
def auth_pages(authenticated_page: Page) -> Pages:
    """API-authenticated Pages facade — primary, fast."""
    return Pages(authenticated_page)


@pytest.fixture(scope="function")
def auth_pages_ui(authenticated_page_ui: Page) -> Pages:
    """UI-authenticated Pages facade — fallback for tests that navigate heavily."""
    return Pages(authenticated_page_ui)
