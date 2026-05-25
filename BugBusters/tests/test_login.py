

def test_login_flow(app):
    app.auth.open_login_form()
    app.auth.login(app.data.EMAIL, app.data.PASSWORD)
    app.page.wait_for_load_state("networkidle")
    app.auth.should_have_profile_link()