from BugBusters.data.constants import Constants

def test_create_event_page(app):
    app.event_create.navigate(f"{Constants.BASE_URL}/events/create")
    app.event_create.fill_creation_form("Party")