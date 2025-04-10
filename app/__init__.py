import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('app.config.Config')
    app.config['JSON_SORT_KEYS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    from .routes.authentication import authentication_blueprint
    from .routes.rest_api import rest_api_bp

    # Register Blueprints
    app.register_blueprint(authentication_blueprint)
    app.register_blueprint(rest_api_bp)

    @app.route('/', methods=['GET'])
    def login_page():
        return render_template('login.html')
    
    return app

# # This is the function used by Flask-Login to load the user from the database
@login_manager.user_loader
def load_user(user_id):
    from .models import User
    return User.query.get(int(user_id))
