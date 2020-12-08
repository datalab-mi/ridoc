"""Initialize app."""
from flask import Flask, g
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from .authentication import authenticate, identity, User, users, username_table, userid_table 



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.debug = True


    # Application Configuration
    app.config.from_object('config.Config')

    #authentification
    jwt = JWT(app, authenticate, identity)

    with app.app_context():
        # Import parts of our application
        from .admin import admin_routes
        from .user import user_routes
        from .common import common_routes

        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(common_routes.common_bp)

        return app
