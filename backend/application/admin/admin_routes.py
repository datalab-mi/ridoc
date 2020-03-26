"""Routes for logged-in account pages."""
import json
from os import environ
from elasticsearch import Elasticsearch
from flask import Blueprint, render_template
from flask import current_app as app

from dotenv import load_dotenv
load_dotenv()

elastic_host = environ.get('Elastic_host')
elastic_port = environ.get('Elastic_port')
client = Elasticsearch([{'host': str(elastic_host), 'port': str(elastic_port)}])

# Blueprint Configuration
admin_bp = Blueprint('admin_bp', __name__,url_prefix='/admin')


@admin_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return json.dumps({"status": "ok"})

@admin_bp.route('/cluster', methods=['GET'])
def cluster():
    elastic_info = Elasticsearch.info(client)
    return json.dumps(elastic_info, indent=4 )
