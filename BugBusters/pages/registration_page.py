import re
from BugBusters.pages.base_page import BasePage



class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.login_btn = page.locator(
            'header button:has(use[href*="phi-caret-down-16"])'
        )

        self.no_account_link = page.locator(
            'button[type="button"].underline'
        )

        self.last_api_response = None

    def navigate_to_registration(self):
        self.login_btn.first.wait_for(state="visible", timeout=5000)
        self.login_btn.first.click()

        self.no_account_link.wait_for(state="visible", timeout=5000)
        self.no_account_link.click()


    def fill_registration_form(self, name, email, password, confirm_password):
        self.page.get_by_placeholder("Name").fill(name)
        self.page.get_by_placeholder("Email").fill(email)

        pass_fields = self.page.get_by_placeholder(re.compile(r"Password", re.IGNORECASE))
        pass_fields.first.fill(password)
        pass_fields.last.fill(confirm_password)

    def submit_registration(self):
        self.page.get_by_role("button", name=re.compile("Sign Up", re.IGNORECASE)).click()

    def register(self, name, email, password, confirm_password):
        self.fill_registration_form(name, email, password, confirm_password)
        with self.page.expect_response(re.compile(r"(register|auth|user)"), timeout=5000) as response_info:
             self.submit_registration()
        self.last_api_response = response_info.value

    def is_registration_successful(self):
        try:

            self.page.get_by_text("Account registered").wait_for(state="visible", timeout=2000)
            return True
        except:
            return False



    def get_error_message(self):

        try:
            if self.last_api_response and self.last_api_response.status >= 400:
                response_json = self.last_api_response.json()


                if "errors" in response_json and len(response_json["errors"]) > 0:
                    clean_error = response_json["errors"][0].get("message")
                    print(f"\n[PLAYWRIGHT API LOG] Распакован чистый текст ошибки: '{clean_error}'")
                    return clean_error

                # Fallback на случай другого формата
                error_text = response_json.get("message") or response_json.get("error") or str(response_json)
                return error_text
        except Exception as e:
            print(f"\n[PLAYWRIGHT API LOG] Не удалось прочитать JSON ответа: {e}")
            try:
                return self.last_api_response.text()
            except:
                return ""