import re
from playwright.sync_api import expect

from BugBusters.pages.profile_page import ProfilePage


def test_profile_sidebar_tabs_are_clickable(authorized_page):
    page = authorized_page
    profile_page = ProfilePage(page)

    profile_page.close_whats_new_popup()

    expect(page).to_have_url(re.compile(r"/en/user/personal-information"))
    expect(profile_page.profile_tab).to_be_visible()

    for tab, expected_url in profile_page.get_sidebar_tabs():
        expect(tab).to_be_visible()
        expect(tab).to_be_enabled()

        tab.click()
        page.wait_for_load_state("networkidle")

        profile_page.close_whats_new_popup()

        expect(page).to_have_url(re.compile(expected_url))
        expect(page.locator("body")).to_be_visible()


