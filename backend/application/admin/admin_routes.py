import json
from pathlib import Path  # python3 only
import pandas as pd
from os import environ

from flask import current_app as app
from flask import Blueprint, render_template, request, make_response, abort, jsonify, send_from_directory

from tools.elastic import create_index, inject_documents
from tools.elastic import index_file as elastic_index_file
from tools.elastic import delete_file as elastic_delete_file

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','md'}

# Blueprint Configuration
admin_bp = Blueprint('admin_bp', __name__,url_prefix='/admin')

print(app.config)

@admin_bp.route('/cluster', methods=['GET'])
def cluster():
    elastic_info = Elasticsearch.info(client)
    return json.dumps(elastic_info, indent=4 )



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@admin_bp.route("/<filename>", methods=["PUT","DELETE"])
def upload_file(filename: str):

    path_file = Path(app.config['USER_DATA']) / app.config['PDF_DIR'] / filename
    path_meta = Path(app.config['USER_DATA']) / app.config['META_DIR'] / filename
    path_json = Path(app.config['USER_DATA']) / app.config['JSON_DIR'] / filename

    path_meta = path_meta.with_suffix('').with_suffix('.json') # replace extension
    path_json = path_json.with_suffix('').with_suffix('.json') # replace extension


    if request.method == 'DELETE':
        if path_file.exists():
            path_file.unlink()
            path_meta.unlink(missing_ok=True)
            path_json.unlink(missing_ok=True)
            return make_response(jsonify(sucess=True), 204)

        else:
            return make_response(jsonify(sucess=False), 404)

    elif request.method == 'PUT':
        if path_file.exists():
            status = 200
        else:
            status = 201

        # ? check if the post request has the file part ?
        file = request.files.get('file', False)
        # if user does not select file, browser also
        # submit an empty part without filename

        if file and allowed_file(filename):
            # save file
            file.save(path_file)
        # save meta
        with open(path_meta , 'w', encoding='utf-8') as f:
            json.dump(request.form, f, ensure_ascii=False)

        return  make_response(jsonify(sucess=True), status)

    else:
        abort(500)


@admin_bp.route("/<index_name>/_doc/<filename>", methods=["DELETE", "PUT"])
def index_file(index_name: str, filename: str):
    #index_name = request.args.get('index_name',None)
    #filename = request.args.get('filename',None)

    if not index_name or not filename:
        print('Missing keys')
        return abort(500)
    if request.method == 'PUT':
        res = elastic_index_file(filename, index_name,
                    app.config['USER_DATA'],
                    app.config['PDF_DIR'],
                    app.config['JSON_DIR'],
                    app.config['META_DIR'])
        status = 201 if res['result'] == 'created' else 200 if res['result'] == 'updated' else 500
        return make_response(res, status)

    elif request.method == 'DELETE':
        status, res = elastic_delete_file(filename, index_name)
        return make_response(res, status)


@admin_bp.route('/index', methods=['GET'])
def index():
    """(Re)index after a mapping change
    """
    content = request.get_json(force=True)
    index_name = content.get('index_name', app.config['NOM_INDEX'])

    create_index(app.config['NOM_INDEX'],
                 app.config['USER_DATA'],
                 app.config['ES_DATA'],
                 app.config['MAPPING_FILE'],
                 app.config['GLOSSARY_FILE'],
                 app.config['EXPRESSION_FILE'])

    # inject only json
    META_DIR = Path(app.config['USER_DATA']) / app.config['PDF_DIR'] / metada_file

    inject_documents(index_name,
                    app.config['USER_DATA'],
                    pdf_path = app.config['PDF_DIR'],
                    json_path = app.config['JSON_DIR'],
                    metada_file = META_DIR)

    return jsonify(success=True)

@admin_bp.route("/synonym/<key>", methods=["DELETE", "PUT"])
def synonym(key: str):
    body = request.get_json(force=True)

    glossary_file = Path(app.config['USER_DATA']) / app.config['GLOSSARY_FILE']
    if not body[0]['value'] or not body[1]['value']:
        print('Missing keys')
        return abort(500)

    if glossary_file.exists():
        glossary_df = pd.read_csv(glossary_file, sep='=>',header=None, names=['value','key']);

    else:
        return abort(500)

    if request.method == 'PUT':
        if key in glossary_df['key'].tolist():
            status = 200
            glossary_df.loc[glossary_df['key'] == key, 'value'] = body[1]['value']
        else:
            status = 201
            glossary_df = pd.concat([pd.DataFrame( {'key': key, 'value': body[1]['value']},index=[0]),
                                    glossary_df],ignore_index=True)

        content = []
        for _, row in glossary_df.iterrows():
            content += [row['value'] + '=>' + row['key']]
        glossary_file.write_text('\n'.join(content))
            #to_csv(glossary_file, sep=str('=>'),header=False, index=False, encoding='utf-8')
        return make_response(glossary_df.to_json(orient='records'), status)

    elif request.method == 'DELETE':
        return make_response(res, status)

    return
