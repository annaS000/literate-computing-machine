# __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models after db is initialized
    from app.models import User, Client, Token

    # Register blueprints
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
