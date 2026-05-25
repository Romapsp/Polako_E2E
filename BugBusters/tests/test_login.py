

def test_login_flow(app, login_user_data):
    app.auth.open_login_form()
    app.auth.login(**login_user_data)
    app.auth.should_have_profile_link()