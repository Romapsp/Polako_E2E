import json
import os
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright
from bughunters.data.constants import MANAGER_USER, TIMEOUTS, URLS
from bughunters.pages import Pages

API_LOGIN_URL = "https://stg.polakohedonist.club/api/auth/login"

# "What's new" modal selectors — used in conftest before page objects are available
_MODAL_OVERLAY   = "div.fixed.inset-0.z-50"
_MODAL_CLOSE_BTN = "div[role='dialog'] button[type='button'][class*='border-gray-200']"


def _dismiss_modal(page: Page, timeout: int = 3_000) -> None:
    """Dismiss the announcement modal if visible. Safe to call at any time."""
    try:
        page.locator(_MODAL_OVERLAY).wait_for(state="visible", timeout=timeout)
    except Exception:
        return
    try:
        page.locator(_MODAL_CLOSE_BTN).click(timeout=2_000)
        page.locator(_MODAL_OVERLAY).wait_for(state="hidden", timeout=5_000)
    except Exception:
        page.keyboard.press("Escape")
        try:
            page.locator(_MODAL_OVERLAY).wait_for(state="hidden", timeout=3_000)
        except Exception:
            pass


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


# ── UI-based auth (primary) ───────────────────────────────────────────────────
#
# UI login is the only approach that fully initialises the Next.js session
# (sets access_token, content_helper_token, pha_refresh cookies + localStorage).
# API-only cookie injection breaks CSR navigation between authenticated pages.

def _ui_login(page: Page) -> None:
    """
    Login via the header modal, then navigate to personal-information.
    Language-independent: structural selectors only.
    """
    page.goto(URLS["home"], timeout=TIMEOUTS["navigation"])
    page.locator("button.ml-4").click()
    page.locator("input[name='email']").fill(MANAGER_USER["email"])
    page.locator("input[name='password']").fill(MANAGER_USER["password"])
    page.locator("button[type='submit'].btn-accent").click()
    page.locator("a[href*='/user']").first.wait_for(
        state="visible", timeout=TIMEOUTS["navigation"]
    )
    # Go straight to the page under test and dismiss the announcement modal
    page.goto(URLS["personal_info"], timeout=TIMEOUTS["navigation"])
    _dismiss_modal(page)


@pytest.fixture(scope="function")
def authenticated_page(browser_instance: Browser) -> Page:
    """
    Primary fixture: UI login → personal-information page, modal dismissed.
    Each test gets a fresh authenticated context.
    """
    ctx = browser_instance.new_context(viewport={"width": 1280, "height": 800})
    ctx.set_default_timeout(TIMEOUTS["default"])
    p = ctx.new_page()
    _ui_login(p)
    yield p
    ctx.close()


# ── API-based auth (fallback / for auth tests only) ───────────────────────────
#
# Suitable only for tests that stay on personal-information without navigating away.
# Does NOT support CSR navigation to other /user/* pages.

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
        state="visible", timeout=TIMEOUTS["element"]
    )
    _dismiss_modal(page)
    return page, ctx


@pytest.fixture(scope="function")
def authenticated_page_api(browser_instance: Browser) -> Page:
    """
    Fallback fixture: API login via cookie injection.
    Use only for tests on personal-information that do NOT navigate away.
    """
    page, ctx = _api_login(browser_instance)
    yield page
    ctx.close()


# ── Page-object facades ───────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def pages(page: Page) -> Pages:
    return Pages(page)


@pytest.fixture(scope="function")
def auth_pages(authenticated_page: Page) -> Pages:
    """UI-authenticated pages facade — supports full navigation."""
    return Pages(authenticated_page)


@pytest.fixture(scope="function")
def auth_pages_ui(authenticated_page: Page) -> Pages:
    """Alias for auth_pages — kept for backward compatibility."""
    return Pages(authenticated_page)


@pytest.fixture(scope="function")
def auth_pages_api(authenticated_page_api: Page) -> Pages:
    """API-authenticated pages facade — personal-info only."""
    return Pages(authenticated_page_api)
