from TP_Polako_E2E.pages.profile.user_profile_page import UserProfilePage

TOP_WARNING_BANNER = "div.bg-amber-50"
FILL_DATA_BTN = 'div.bg-amber-50 a[href*="contract-data"]'
CREATE_CONTRACT_BTN = 'div.bg-amber-50 a[href*="contracts"]'

MANAGER_ROLE_BADGE = "main div.gap-1 > div > span:nth-of-type(1)"
COMMISSION_BADGE = "main div.gap-1 > div > span:nth-of-type(2)"

COMPANY_BTN = 'nav a[href*="company"]'
MANAGE_EVENTS_BTN = 'nav a[href*="events"]'
CONTRACT_DATA_BTN = 'nav a[href*="contract-data"]'
CONTRACTS_BTN = 'nav a[href*="contracts"]'
REPORTS_BTN = 'nav a[href*="reports"]'
QR_CODE_BTN = 'nav a[href*="qr-generator"]'
WITHDRAW_BTN = 'nav a[href*="withdraw"]'
PUBLICATIONS_BTN = 'nav a[href*="publications"]'
MANAGE_BTN = 'nav a[href*="manage"]'

CLOSE_MODAL_BTN = 'div.fixed.inset-0 button'


class ManagerProfilePage(UserProfilePage):
    # BADGES
    def verify_user_role_badge(self):
        self.page.locator(MANAGER_ROLE_BADGE).wait_for(state="visible", timeout=4000)

    def verify_commission_badge_visible(self, timeout: int = 3000):
        self.page.locator(COMMISSION_BADGE).wait_for(state="visible", timeout=timeout)

    def get_commission_text(self) -> str:
        return self.page.locator(COMMISSION_BADGE).text_content().strip()

    # WARNING BANNER
    def verify_warning_banner_visible(self, timeout: int = 3000):
        self.page.locator(TOP_WARNING_BANNER).wait_for(state="visible", timeout=timeout)

    def click_banner_fill_data(self):
        self.page.locator(FILL_DATA_BTN).click()

    def click_banner_create_contract(self):
        self.page.locator(CREATE_CONTRACT_BTN).click()

    # SIDEBAR
    def click_company_btn(self):
        self.page.locator(COMPANY_BTN).click()

    def verify_company_btn_visible(self):
        self.page.locator(COMPANY_BTN).wait_for(state="visible")

    def click_event_management_link(self):
        self.page.locator(MANAGE_EVENTS_BTN).click()

    def force_click_event_management_link(self):
        link = self.page.locator(MANAGE_EVENTS_BTN)
        link.wait_for(state="visible", timeout=500)
        for _ in range(5):
            link.click(force=True)
            self.page.wait_for_timeout(500)

    def verify_event_management_link_visible(self):
        self.page.locator(MANAGE_EVENTS_BTN).wait_for(state="visible")

    def click_contract_data_btn(self):
        self.page.locator(CONTRACT_DATA_BTN).click()

    def verify_contract_data_btn_visible(self):
        self.page.locator(CONTRACT_DATA_BTN).wait_for(state="visible")

    def click_contracts_btn(self):
        self.page.locator(CONTRACTS_BTN).click()

    def verify_contracts_btn_visible(self):
        self.page.locator(CONTRACTS_BTN).wait_for(state="visible")

    def click_reports_btn(self):
        self.page.locator(REPORTS_BTN).click()

    def verify_reports_btn_visible(self):
        self.page.locator(REPORTS_BTN).wait_for(state="visible")

    def click_qr_code_btn(self):
        self.page.locator(QR_CODE_BTN).click()

    def verify_qr_code_btn_visible(self):
        self.page.locator(QR_CODE_BTN).wait_for(state="visible")

    def click_withdraw_btn(self):
        self.page.locator(WITHDRAW_BTN).click()

    def verify_withdraw_btn_visible(self):
        self.page.locator(WITHDRAW_BTN).wait_for(state="visible")

    def click_publications_btn(self):
        self.page.locator(PUBLICATIONS_BTN).click()

    def verify_publications_btn_visible(self):
        self.page.locator(PUBLICATIONS_BTN).wait_for(state="visible")

    def click_manage_btn(self):
        self.page.locator(MANAGE_BTN).click()

    def verify_manage_btn_visible(self):
        self.page.locator(MANAGE_BTN).wait_for(state="visible")

    def close_modal(self):
        modal = self.page.locator(CLOSE_MODAL_BTN)
        try:
            if modal.is_visible(timeout=5000):
                modal.click()
        except:
            pass