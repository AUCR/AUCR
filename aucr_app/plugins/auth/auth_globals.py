from sqlalchemy.exc import OperationalError
from aucr_app import db, create_app
from aucr_app.plugins.auth.models import Groups

app = create_app()
db.init_app(app)

with app.app_context():
    count = 0
    items_available_choices_list = []
    try:
        group_data = Groups.query.all()
    except OperationalError:
        group_data = {"admin": 0, "user": 1, "system": 2}
    except TypeError:
        # Default to basic User dict if database is not available.
        group_data = {"admin": 0, "user": 1, "system": 2}
    for items in group_data:
        count += 1
        new_list = (str(count), items)
        items_available_choices_list.append(new_list)
    AVAILABLE_CHOICES = items_available_choices_list
