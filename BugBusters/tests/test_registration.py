import uuid



# =============================================================================
# ТЕСТ 1: Успешная регистрация (Позитивный сценарий)
# =============================================================================
def test_successful_registration(app):
    app.registration.navigate_to_registration()
    dynamic_email = f"qa_user_{uuid.uuid4().hex[:5]}@gmail.com"


    app.registration.register(
        name=app.data.USER_NAME,
        email=dynamic_email,
        password=app.data.PASSWORD,
        confirm_password=app.data.PASSWORD
    )


    assert app.registration.last_api_response.status in [200, 201,204]


# =============================================================================
# ТЕСТ 2: Регистрация существующего пользователя (Негативный сценарий)
# =============================================================================
def test_failed_registration_duplicate_email(app):
    app.registration.navigate_to_registration()
    duplicate_email = app.data.EMAIL

    app.registration.register(
        name=app.data.USER_NAME,
        email=duplicate_email,
        password=app.data.PASSWORD,
        confirm_password=app.data.PASSWORD
    )


    assert app.registration.last_api_response.status in [400, 409], \
        "Ошибка: система зарегистрировала дубликат!"