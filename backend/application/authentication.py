import json, os
from functools import wraps
from pathlib import Path
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    JWTManager, verify_jwt_in_request, verify_jwt_in_request_optional,
    create_access_token,
    get_jwt_claims,
    jwt_required, get_jwt_identity
)

from flask import current_app as app
from flask import jsonify, request

class User(object):
    def __init__(self, id, username, password, role=None):
        self.id = id
        self.username = username
        self.password = password
        self.role = role
    def __str__(self):
        return "User(id='%s')" % self.id

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

# runtime
jwt = JWTManager()

if "AUTH_DIR" not in app.config:
    auth_dir = Path(__file__).resolve().parent / 'user_database.json'
else:
    auth_dir = Path(app.config["AUTH_DIR"])

with open(auth_dir) as json_file:
    user_database = json.load(json_file)

#auth_bp = Blueprint('auth_bp', __name__,url_prefix='')


users = [User(u['id'], u['username'], u['password'], u.get("role","visitor")) for u in user_database["user_database"]]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}
rules_table = user_database["rules"] if "rules" in user_database else {k:k for k in ["admin", "user", "visitor"]}

# define auth route and decorators
@app.route('/auth', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400
    if username not in username_table:
        return jsonify({"msg": "Username unknown"}), 400
    if username_table[username].password != password :
        return jsonify({"msg": "Bad username or password"}), 401
    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=username_table[username].role)
    return jsonify(access_token=access_token), 200

@app.route('/authorized_resource', methods=['GET'])
@jwt_required
def authorized_resource():
    """ If valid token, return role and
    row of matrice role, ie the authorized resources
    """
    current_role = get_jwt_identity()
    return jsonify(role=current_role,
                   resource=rules_table[current_role]), 200
# Admin check
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "admin" in rules_table["visitor"]: #
            print("Do not check token validity")
            return fn(*args, **kwargs)
        else:
            verify_jwt_in_request()
            claim = get_jwt_claims()
            #print("claim role : %s"%claim["role"])
            #print("can access to %s"%rules_table[claim["role"]])
            if "admin" not in rules_table[claim["role"]]:
                return jsonify(msg='Admins only, you are %s'%claim["role"]), 403
            else:
                return fn(*args, **kwargs)
    return wrapper

# user check
def user_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if "user" in rules_table["visitor"]: #
            print("Do not check token validity")
            return fn(*args, **kwargs)
        else:
            verify_jwt_in_request()
            claim = get_jwt_claims()
            #print("claim role : %s"%claim["role"])
            #print("can access to %s"%rules_table)
            if "user" not in rules_table[claim["role"]]:
                return jsonify(msg='Admins or users only, you are %s'%claim["role"]), 403
            else:
                return fn(*args, **kwargs)
    return wrapper

@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {"role": identity}
