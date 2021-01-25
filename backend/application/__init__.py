"""Initialize app."""
from flask import Flask

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.debug = True

    # Application Configuration
    app.config.from_object('config.Config')



    with app.app_context():
        # Import parts of our application
        from .authentication import jwt
        from .admin import admin_routes
        from .user import user_routes
        from .visitor import visitor_routes
        jwt.init_app(app)

        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(user_routes.user_bp)
        app.register_blueprint(visitor_routes.visitor_bp)
        return app
