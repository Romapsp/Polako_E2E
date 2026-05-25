from BugBusters.pages.base_page import BasePage


class RegistrationPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.login_btn = page.locator(
            'header button:has(use[href*="phi-caret-down-16"])'
        )

        self.no_account_link = page.locator(
            'button.text-center.text-sm.text-black.underline.underline-offset-2'
        )

        self.email_input = page.locator(
            'form input[name="email"]'
        )

        self.password_input = page.locator(
            'form input[name="password"]'
        )

        self.name_input = page.locator(
            'form input[name="first_name"]'
        )

        self.submit_button = page.locator(
            'form button[type="submit"]'
        )

        self.last_api_response = None

    def navigate_to_registration(self):
        self.login_btn.first.wait_for(state="visible", timeout=5000)
        self.login_btn.first.click()

        self.no_account_link.wait_for(state="visible", timeout=5000)
        self.no_account_link.click()

    def fill_registration_form(self, name, email, password):
        self.name_input.fill(name)
        self.email_input.fill(email)
        self.password_input.fill(password)

    def submit_registration(self):
        self.submit_button.wait_for(state="visible", timeout=5000)
        self.submit_button.click()

    def register(self, name, email, password):
        self.fill_registration_form(name, email, password)


        with self.page.expect_response(
                lambda response: (
                        "/api/auth/signup" in response.url
                        and response.request.method == "POST"
                ),
                timeout=5000
        ) as response_info:
            self.submit_registration()
        self.last_api_response = response_info.value

    def is_registration_successful(self):
        return (
                self.last_api_response is not None
                and self.last_api_response.status in [200, 201, 204]
        )

    def get_error_message(self):
        try:
            if self.last_api_response and self.last_api_response.status >= 400:
                response_json = self.last_api_response.json()

                if "errors" in response_json and len(response_json["errors"]) > 0:
                    clean_error = response_json["errors"][0].get("message")

                    print(
                        f"\n[PLAYWRIGHT API LOG] "
                        f"Распакован чистый текст ошибки: '{clean_error}'"
                    )

                    return clean_error

                return (
                        response_json.get("message")
                        or response_json.get("error")
                        or str(response_json)
                )

        except Exception as e:
            print(
                f"\n[PLAYWRIGHT API LOG] "
                f"Не удалось прочитать JSON ответа: {e}"
            )

            try:
                return self.last_api_response.text()


            except Exception:

                return ""
