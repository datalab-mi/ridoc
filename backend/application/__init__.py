"""Initialize app."""
from flask import Flask
import os
from dotenv import load_dotenv
from flask_cors import CORS

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)

    # Application Configuration
    app.config.from_object('config.Config')

    with app.app_context():
        # Import parts of our application
        from .admin import admin_routes
        from .user import user_routes
        from .common import common_routes

        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(common_routes.common_bp)

        return app
