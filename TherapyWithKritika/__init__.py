from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "Client_Data.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hogayabhai hogayabhai'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .home import home_page
    from .auth import validate

    app.register_blueprint(home_page, url_prefix="/")
    app.register_blueprint(validate, url_prefix="/")

    from .model_db import Client

    with app.app_context():
        db.create_all()

    return app

def create_db(app):
    if not path.exists('MINI_WEBSITE/' + DB_NAME):
        #db.create_all()
        print('Database Created')