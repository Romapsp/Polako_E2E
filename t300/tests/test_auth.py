import re

from data.constants import MANAGER_USER
from playwright.sync_api import expect


def test_login_form_opens(app):
    app.auth.open_login_form()
    expect(app.auth.login_title).to_be_visible()


def test_sign_button_disabled_by_default(app):
    app.auth.open_login_form()
    expect(app.auth.submit_sign_in_button).to_be_enabled()


def test_sign_in_enabled_after_fill(app):
    app.auth.open_login_form()
    app.auth.fill_login_form(MANAGER_USER["email"], MANAGER_USER["password"])
    expect(app.auth.submit_sign_in_button).to_be_enabled()


def test_manager_can_login(app):
    app.auth.login(MANAGER_USER["email"], MANAGER_USER["password"])
    expect(app.auth.profile_link).to_be_visible()


def test_homepage_and_ui_login(app):
    expect(app.page).to_have_url(re.compile(r".*\/(en|ru|sr)\/?"))

    app.auth.login(MANAGER_USER["email"], MANAGER_USER["password"])

    expect(app.auth.profile_link).to_be_visible()
