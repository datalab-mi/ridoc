import json
from pathlib import Path
from werkzeug.security import safe_str_cmp
import os

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

if "AUTH_DIR" not in os.environ:
    auth_dir = Path(__file__).resolve().parent / 'user_database.json'
else:
    auth_dir = Path(os.environ["AUTH_DIR"])

with open(auth_dir) as json_file:
    user_database = json.load(json_file)["user_database"]


users = [User(u['id'], u['username'], u['password']) for u in user_database]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)
