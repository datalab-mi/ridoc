import json, os
from pathlib import Path  # python3 only
import pandas as pd
import time

from flask import Blueprint, render_template, request, make_response, abort, jsonify, send_from_directory
from flask import current_app as app

from application.authentication import user_required
from tools.elastic import search as elastic_search
from tools.elastic import build_query as elastic_build_query
from tools.elastic import suggest as elastic_suggest
from tools.elastic import get_file as elastic_get_file
from tools.elastic import get_unique_keywords

# Blueprint Configuration
user_bp = Blueprint('user_bp', __name__,url_prefix='/user')
# USER_DATA is known by parent script __init__
if not Path(app.config['USER_DATA']).exists():
    Path(app.config['USER_DATA']).mkdir(parents=True) # recursive


@user_bp.route("/files")
@user_bp.route("/files/<path:path>")
@user_required
def get_file(path=''):
    """Get a file or folder name in the file system USER_DATA
    Args:
        path (str): The relative path of the document or folder to get
    Returns:
        list: List of files if path is a path
        binary: The file if path is a file
    """

    dir = Path(app.config['USER_DATA']) / path
    if dir.is_file():
        return send_from_directory(app.config['USER_DATA'], path, as_attachment=True)

    elif dir.is_dir():
        files = []
        for filename in dir.glob("**/*"):
            if filename.is_file():
                #filename = Path(filename).relative_to(Path(app.config['USER_DATA']))
                #dict(modified = os.path.getmtime(filename),
                #key=str(filename)
                files.append(dict(name=str(filename.relative_to(Path(dir))),
                                  lastModified=time.ctime(round(filename.stat().st_mtime)),
                                  size="%d kB"%( filename.stat().st_size * 1024//10e3)) ) # k bytes to kB

        return jsonify(files)
    else:
        # try to infer the extention
        for filename in dir.parent.glob(dir.stem + "*"):
            return send_from_directory(app.config['USER_DATA'],
                filename.relative_to(Path(app.config['USER_DATA'])),
                as_attachment=True)

        return make_response('%s not found'%dir, 404)


@user_bp.route('/search', methods=['POST'])
@user_required
def search():
    """ ES search
    Args:
        body (json): The ES clauses (must, shoud, filter)
    Returns:
        list: List of results
    """

    content = request.get_json(force=True)
    must = content.get('must', None)
    should = content.get('should', None)
    filter = content.get('filter', None)
    highlight = content.get('highlight', None)

    index_name = content.get('index_name', None)
    if  not index_name:
        return

    GLOSSARY_FILE = app.config['GLOSSARY_FILE']
    EXPRESSION_FILE = app.config['RAW_EXPRESSION_FILE']
    USER_DATA = app.config['USER_DATA']
    THRESHOLD_FILE = app.config['THRESHOLD_FILE']

    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / EXPRESSION_FILE
    threshold_file = Path(USER_DATA) / THRESHOLD_FILE

    res = elastic_search(must, should, filter, index_name, highlight,
                glossary_file = glossary_file,
                expression_file = expression_file,
                threshold_file = threshold_file)

    return json.dumps(res)

@user_bp.route('/synonym', methods=['GET'])
@user_required
def synonym():
    """ Get the synonym file
    """

    filename = request.args.get('filename', app.config['GLOSSARY_FILE'])
    synonym_file = Path(app.config['USER_DATA']) / (filename + '.txt')

    if "glossaire" in filename:
        names = ['expressionB','expressionA']
        sep = ' => '
    elif "expression" in filename:
        names = ['expressionA']
        sep = ';'
    else:
        return abort(501)

    if synonym_file.exists():
        synonym_df = pd.read_csv(synonym_file, header=None, sep=sep, names=names);
        synonym_df['key'] = synonym_df.index + 1
        return make_response(synonym_df.to_json(orient='records'), 200)

    # In the other cases
    return make_response('', 404)

@user_bp.route('/suggest', methods=['POST'])
@user_required
def suggest():
    """ ES suggestion
    Args:
        request (json)
    Returns:
        list: List of suggestions
    """
    content = request.get_json(force=True)
    user_entry = content.get('content', None)
    index_name = content.get('index_name', None)
    fields = content.get('fields', [])
    res = []
    for field in fields:
        res += elastic_suggest(user_entry,
                    index_name, field=field)

    return json.dumps(res)#.encode('utf8')

@user_bp.route("/logo", methods=['GET'])
@user_required
def get_logo(name='logo.svg'):
    """Get the logo in the file system USER_DATA
    Args:
        path (str): The relative path of the document or folder to get
    Returns:
        file: Logo file
    """
    filename  = (Path(app.config['USER_DATA']) / app.config['LOGO'])
    print(filename)

    if filename.is_file(): # return first found
        return send_from_directory(app.config['USER_DATA'], app.config['LOGO'], as_attachment=True)
    else:
        return make_response(str(Path(app.config['USER_DATA']) / name), 404)

@user_bp.route("/keywords/<index_name>/<field>", methods=['GET'])
@user_required
def get_keywords(index_name: str, field: str):
    """"Wrap get_unique_keywords function
    Get unique keywords list from an filed of type keyword
    """
    keyword_list = get_unique_keywords(index_name, field)
    return jsonify(keyword_list)

@user_bp.route("/<index_name>/_doc/<filename>", methods=["GET"])
@user_required
def index_file(index_name: str, filename: str):
    """Get a document in Elastic Search (ES)
    Args:
        index_name (str): ES index
        filename (str): The file name
        _source_includes (str): optional url argument, Required fields separated
        with comma
    """

    if not index_name or not filename:
        print('Missing keys')
        return abort(500)
    source_includes = request.args.get('_source_includes', '')
    source_includes = source_includes.split(",")
    res = elastic_get_file(index_name, filename, source_includes)
    return jsonify(res['_source'])
