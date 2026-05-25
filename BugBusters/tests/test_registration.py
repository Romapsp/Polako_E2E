


# =============================================================================
# ТЕСТ 1: Успешная регистрация (Позитивный сценарий)
# =============================================================================
def test_successful_registration(app, new_user_data):
    app.registration.navigate_to_registration()

    app.registration.register(**new_user_data)

    assert app.registration.last_api_response.status in [200, 201, 204]


# =============================================================================
# ТЕСТ 2: Регистрация существующего пользователя (Негативный сценарий)
# =============================================================================
def test_failed_registration_duplicate_email(app, existing_user_data):
    app.registration.navigate_to_registration()

    app.registration.register(**existing_user_data)

    assert app.registration.last_api_response.status in [400, 409]
    assert app.registration.get_error_message()