"""Initialize app."""
from flask import Flask, g
from flask_jwt import JWT, jwt_required, current_identity
#from security import authenticate, identity
#import database_user



def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.debug = True

    class User(object):
        def __init__(self, id, username, password):
            self.id = id
            self.username = username
            self.password = password

        def __str__(self):
            return "User(id='%s')" % self.id

    users = [
        User(1, 'user1', 'abcxyz'),
        User(2, 'user2', 'abcxyz'),
    ]

    username_table = {u.username: u for u in users}
    userid_table = {u.id: u for u in users}
    
    #Security
    def authenticate(username, password):
        user = username_table.get(username, None)
        if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
            return user

    def identity(payload):
        user_id = payload['identity']
        return userid_table.get(user_id, None)

    

    #authentification
    app.secret_key = "jose"  # Make this long, random, and secret in a real app!
    jwt = JWT(app, authenticate, identity)


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
