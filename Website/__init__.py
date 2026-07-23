from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from os.path import dirname, abspath
from flask_login import LoginManager

# Database
db = SQLAlchemy()
DB_NAME = "database.db"



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dudududumaxverstapen' # just a random string of letters
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{path.join(dirname(abspath(__file__)), DB_NAME)}' # tells where to create the database
    db.init_app(app) #tells flask that we are using this database

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

def create_database(app): #checks if database exists, if not then it creates one
    if not path.exists(path.join(dirname(abspath(__file__)), DB_NAME)):
        with app.app_context():
            db.create_all()
        print('Created Database!')
