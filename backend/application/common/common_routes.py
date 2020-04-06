"""Routes for logged-in account pages."""
import json, os
from pathlib import Path  # python3 only

from flask import Blueprint, render_template, request, make_response, jsonify
from flask import current_app as app

from tools.elastic import search as elastic_search
from tools.elastic import build_query as elastic_build_query

from elasticsearch import Elasticsearch
es = Elasticsearch()
# Blueprint Configuration
common_bp = Blueprint('common_bp', __name__,url_prefix='/common')

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
    Build only the custom query. The
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
