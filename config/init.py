from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("db_uri")
    app.config['SECRET_KEY'] = os.getenv("secret_key")
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=3)
    app.config
    db.init_app(app)
    jwt.init_app(app)
    return app





