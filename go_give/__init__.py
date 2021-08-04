from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_babel import Babel, lazy_gettext as _l
from .admin import add_admin


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
babel = Babel()


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)

    bootstrap = Bootstrap(app)


    app.config['SECRET_KEY'] = 'secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)
    bootstrap = Bootstrap(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    babel.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    add_admin(app, db)
    return app