

def test_successful_login_flow(app, login_user_data):
    app.auth.open_login_form()
    app.auth.login(
        email=login_user_data['email'],
        password=login_user_data['password']
    )

    app.auth.should_have_profile_link()
    app.auth.should_have_avatar_circle(user_name=login_user_data['name'])