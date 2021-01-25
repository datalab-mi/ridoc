"""Routes for logged-in account pages."""
import json

from flask import Blueprint, render_template
from flask import current_app as app

# Blueprint Configuration
visitor_bp = Blueprint('visitor_bp', __name__,url_prefix='/')

@visitor_bp.route('/healthcheck', methods=['GET'])
def healthcheck():
    return json.dumps({"status": "ok"})
