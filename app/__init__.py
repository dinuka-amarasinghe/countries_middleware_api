from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    # Register Blueprints
    from .routes.auth import auth_bp
    from .routes.api import api_bp
    from .routes.admin import admin_bp
    from .routes.base import base_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(base_bp)

    return app
