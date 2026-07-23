from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
from os.path import dirname, abspath
import os

# Database
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-fallback-key')

    # Database: Use PostgreSQL if DATABASE_URL env var is set (production), else SQLite (local dev)
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        # Render provides postgres:// but SQLAlchemy needs postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(dirname(abspath(__file__)), DB_NAME)}'

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # For local SQLite, check if the database file exists
    if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
        if not path.exists(path.join(dirname(abspath(__file__)), DB_NAME)):
            with app.app_context():
                db.create_all()
            print('Created Database!')
    else:
        # PostgreSQL: tables are created automatically on Render
        with app.app_context():
            db.create_all()
        print('Database tables created/verified!')