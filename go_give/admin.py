from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


def add_admin(app, db):
    from .models import User, Message
    admin = Admin(app, name='microblog', template_mode='bootstrap3')
    # Add administrative views here
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Message, db.session))
    return admin
