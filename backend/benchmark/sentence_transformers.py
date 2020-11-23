import argparse
import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green, create_index, put_alias, inject_documents, search, index_file, suggest, build_query
import elasticsearch
from elasticsearch import Elasticsearch, helpers
from benchmark.utils import *
from sentence_transformers import SentenceTransformer

'''Getting the arguments
- the path of the Q/A test base
- the path of the environment (ex: .env-bld)
- the list of the metrics
'''

#Parsing argument
parser = argparse.ArgumentParser(description='Evaluation of the metrics')
parser.add_argument('-base-path',dest='base_path', type=str,
    help='Base path ', default = str(Path(__file__).resolve().parent)) # defaut to current path
parser.add_argument('-qr', dest='qr_path', type=str,
    help='the path to Q/A test base file, ex: QR_file.ods', default = 'QR_file.ods')
parser.add_argument('-env', dest='dotenv_path', type=str,
    help='the path to env file, ex: .env-bld', default = '.env-bld')
parser.add_argument('-m', dest='metric', type=str,
    help='metric to evaluate, ex: dcg', default = 'dcg')


def main(args):
    args.base_path = Path(args.base_path)
    #Loading the environment
    load_dotenv(dotenv_path=args.base_path / args.dotenv_path, override=True)
    INDEX_NAME = os.getenv('INDEX_NAME')

    USER_DATA = os.getenv('USER_DATA')
    ES_DATA = os.getenv('ES_DATA')

    GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
    RAW_EXPRESSION_FILE = os.getenv('RAW_EXPRESSION_FILE')
    MAPPING_FILE =  os.getenv('MAPPING_FILE')
    THRESHOLD_FILE = os.getenv('THRESHOLD_FILE')

    DST_DIR = os.getenv('DST_DIR')
    JSON_DIR = os.getenv('JSON_DIR')
    META_DIR =  os.getenv('META_DIR')

    ES_PORT=os.getenv('ES_PORT')
    ES_HOST=os.getenv('ES_HOST')

    MODEL_NAME = "/app/benchmark/bld/data/sbert.net_models_" + \
        "distilbert-multilingual-nli-stsb-quora-ranking"

    os.makedirs(ES_DATA, exist_ok=True)


    #Reading files
    glossary_file = Path(USER_DATA) / GLOSSARY_FILE
    expression_file = Path(USER_DATA) / RAW_EXPRESSION_FILE
    threshold_file = Path(USER_DATA) / THRESHOLD_FILE

    qr_path = args.base_path /args.qr_path
    if qr_path.suffix in ['.ods']:
        test_base_df = pd.read_excel(qr_path, engine="odf") #if odt file
    elif qr_path.suffix == ".csv":
        test_base_df = pd.read_csv(qr_path, encoding= 'utf-8') #if csv file


    #Instanciation of elasticsearch
    es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

    if es.indices.exists(index=INDEX_NAME):
        for _ in range(3): # to be sure alias and indexes are removed
            es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
            es.indices.delete_alias(index='_all',
                name=INDEX_NAME, ignore=[400, 404])

    # Index creation
    create_index(INDEX_NAME, USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, RAW_EXPRESSION_FILE ) #some parameters are stored in the map, that is linked to the index here

    #Injection of documents
    section = [{'key': 'SITE', 'array':False},
                {'key': 'DIRECTION', 'array':False},
                {'key': 'DOMAINE', 'array':True},
                {'key': 'TITRE', 'array':True},
                {'key': 'Mots clés', 'array':True},
                {'key': 'Date', 'array':True},
                {'key': 'Question', 'array':True},
                {'key': 'Réponse', 'array':False},
                {'key': 'Pièces jointes', 'array':True},
                {'key': 'Liens', 'array':False},
                {'key': 'Références', 'array':False}]


    inject_documents(INDEX_NAME, USER_DATA, DST_DIR, JSON_DIR,
                    meta_path = META_DIR, sections=section)
    time.sleep(1) # ! important, asynchronous injection

    # Embedding with Sentence transformers
    model = SentenceTransformer(MODEL_NAME)
    # Query all documents to retrieve questions
    res = es.search(index=INDEX_NAME, body = {'_source': ['_id', '_type', 'question'],
            'size' : 10000,
            'query': {
                'match_all' : {}
            }
            })

    all_questions={}
    for r in res['hits']['hits']:
        all_questions[r['_id']]= r['_source']['question'][0]

    qids = list(all_questions.keys())
    questions = [all_questions[qid] for qid in qids]

    embeddings = model.encode(questions, show_progress_bar=False)

    # Update the existing index with embedded vectors
    for qid, embedding in zip(qids, embeddings):
        es.update(index=INDEX_NAME,
            doc_type='_doc',
            id=qid,
            body={
                "script" : {
                    "source": "ctx._source.question_vector= params.emb",
                    "lang": "painless",
                    "params" : {
            "emb" : embedding
            }
        }
    })

    time.sleep(1)

    #Searching
    rank_body_requests = []
    rank_body_metric = metric_parameters(args.metric) # building the request metric

    must = {}
    should = {}
    filter = ''
    highlight = []

    #Building the request body
    for index, row in test_base_df.iterrows():
        question_embedding = model.encode(row["Questions"])

        body_query = {
        "query": {
            "script_score": {
            "query": {
                "match_all": {}
            },
            "script": {
                "source": "cosineSimilarity(params.queryVector, 'question_vector') + 1.0",
                "params": {
                "queryVector": question_embedding
                }
            }
            }
        }
        }
        request = { "id": str(index), "request": body_query, "ratings": [{ "_index": INDEX_NAME, "_id": "%s"%row['Fiches'], "rating": 1}]}
        rank_body_requests.append(request)

    import pdb; pdb.set_trace()
    #Metric evaluation
    result = es.rank_eval(body= {
                                  "requests": rank_body_requests,
                                  "metric": rank_body_metric
                                  }, index = INDEX_NAME )
    print(20*'-')
    print('Result of %s script'%Path(__file__).resolve().stem)
    print(20*'-')
    print(json.dumps(result,sort_keys=True, indent=4))
    #import pdb; pdb.set_trace()

    return result
