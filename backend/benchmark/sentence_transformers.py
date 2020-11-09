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
        res = es.search(index=INDEX_NAME, body = {
                '_source': ['_id', '_type', 'question'],
                'size' : 10000,
                'query': {
                    'match_all' : {}
                }
                })
        print(res)
        all_questions={}
        for r in res['hits']['hits']: 
            all_questions[r['_id']]= r['_source']['question'][0]

        qids = list(all_questions.keys())
        questions = [all_questions[qid] for qid in qids]
        
        
        # Embedding
        model = SentenceTransformer('distilbert-multilingual-nli-stsb-quora-ranking')
        
        embeddings = model.encode(questions, show_progress_bar=False)

        bulk_data = []
        for qid, question, embedding in zip(qids, questions, embeddings):
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
