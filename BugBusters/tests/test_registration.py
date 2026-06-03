
# =============================================================================
# ТЕСТ 1: Успешная регистрация (Позитивный сценарий)
# =============================================================================
def test_successful_registration(app, new_user_data):
    app.registration.navigate_to_registration()

    app.registration.register(**new_user_data)

    app.registration.should_have_avatar_circle(user_name=new_user_data['name'])


# =============================================================================
# ТЕСТ 2: Регистрация существующего пользователя (Негативный сценарий)
# =============================================================================
def test_failed_registration_duplicate_email(app, existing_user_data):
    app.registration.navigate_to_registration()

    app.registration.register(**existing_user_data)

    app.registration.should_have_registration_error()
