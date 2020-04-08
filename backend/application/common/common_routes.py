"""Routes for logged-in account pages."""
import json, os
from pathlib import Path  # python3 only

from flask import Blueprint, render_template, request, make_response, jsonify, send_from_directory
from flask import current_app as app
from flask_cors import CORS

from tools.elastic import search as elastic_search
from tools.elastic import build_query as elastic_build_query

from elasticsearch import Elasticsearch
es = Elasticsearch()


# Blueprint Configuration
common_bp = Blueprint('common_bp', __name__,url_prefix='/common')
CORS(common_bp)
# USER_DATA is known by parent script __init__
if not Path(app.config['USER_DATA']).exists():
    Path(app.config['USER_DATA']).mkdir(parents=True) # recursive

@common_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return json.dumps({"status": "ok"})

@common_bp.route("/files/<path:path>")
def get_file(path):
    """Download a file."""
    return send_from_directory(app.config['USER_DATA'], path, as_attachment=True)


@common_bp.route("/files")
def list_files():
    """Endpoint to list files on the server."""
    files = []
    for filename in os.listdir(app.config['USER_DATA']):
        path = Path(app.config['USER_DATA']) / filename
        if path.is_file():
            files.append(filename)
    return jsonify(files)


@common_bp.route("/upload", methods=["POST"])
def post_file():
    """Upload a file."""

    if "/" in filename:
        # Return 400 BAD REQUEST
        abort(400, "no subdirectories directories allowed")

    with (Path(app.config['USER_DATA']) / filename).open() as fp:
        fp.write(request.data)

    # Return 201 CREATED
    return "", 201

# HANDLE CORS
def _build_cors_prelight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@common_bp.route('/index', methods=['GET'])
def index():
    return

@common_bp.route('/build_query', methods=['POST','OPTIONS'])
def build_query():
    """
    Build only the custom query.
    """
    if request.method == "OPTIONS": # CORS preflight
        return _build_cors_prelight_response()
    elif request.method == "POST":

        content = request.get_json(force=True)
        index_name = content.get('index_name', None)
        user_entry = content.get('value', None)
        if not user_entry or not index_name:
            print('Missing keys')
            return json.dumps({})

        GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
        EXPRESSION_FILE = os.getenv('EXPRESSION_FILE')
        USER_DATA = os.getenv('USER_DATA')

        glossary_file = Path(USER_DATA) / GLOSSARY_FILE
        expression_file = Path(USER_DATA) / 'analysed_expression.txt'

        res = elastic_build_query(user_entry,
                    index_name,
                    glossary_file,
                    expression_file)

        seuil = 4.5
        seuil_affichage = 3.5
        print(10*"*")
        print(res)
        return _corsify_actual_response(jsonify(res))

@common_bp.route('/search', methods=['POST'])
def search():
    content = request.json
    user_entry = content.get('value', None)
    index_name = content.get('index_name', None)
    if not user_entry or not index_name:
        return

    GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
    EXPRESSION_FILE = os.getenv('EXPRESSION_FILE')
    USER_DATA = os.getenv('USER_DATA')

    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / 'analysed_expression.txt'

    res = elastic_search(user_entry,
                index_name,
                glossary_file,
                expression_file)

    seuil = 4.5
    seuil_affichage = 3.5
    return json.dumps(res)
