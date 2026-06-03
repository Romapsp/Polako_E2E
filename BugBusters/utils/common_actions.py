from BugBusters.pages.profile_page import ProfilePage
from BugBusters.utils.popups import close_whats_new_popup

def get_page_title(page):
    return page.title()


def reload_profile_page(page):
    page.reload()
    page.wait_for_load_state("networkidle")
    close_whats_new_popup(page)
    return ProfilePage(page)