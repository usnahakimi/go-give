from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    if 'RDS_HOSTNAME' in os.environ:
      DATABASE = {
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
      }
      database_url = 'mysql://%(USER)s:%(PASSWORD)s@%(HOST)s:%(PORT)s/%(NAME)s' % DATABASE
    else:
      database_url = 'sqlite:///' + os.path.join(app.instance_path, 'go_give.sqlite')

    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI = database_url,
        SQLALCHEMY_POOL_RECYCLE = 280,
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User 
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app