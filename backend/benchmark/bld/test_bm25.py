import argparse
import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green, create_index, put_alias, inject_documents, search, index_file, suggest, build_query
import elasticsearch
from elasticsearch import Elasticsearch
from benchmark.utils import *


'''Getting the arguments
- the path of the Q/A test base
- the path of the environment (ex: bld/.env-bld)
- the list of the metrics
backend/benchmark/bld/.env-bld
'''


#Parsing argument
parser = argparse.ArgumentParser(description='Evaluation of the metrics')
parser.add_argument('-qr', dest='test_base_path',type=str,help='the path to Q/A test base file, ex: QR_file.ods', default = 'QR_file.ods')
parser.add_argument('-env',dest='env_path',type=str,help='the path to env file, ex: .env-bld', default = '.env-bld')
parser.add_argument('-m', dest='metrics_list',type=str,help='the list of metrics, ex: DCG Recall',nargs='+', default = ['DCG'])
args = parser.parse_args()

metrics_list = args.metrics_list
env_path_bench = Path('/app/benchmark/bld') / args.env_path
dir_path(env_path_bench)


#Loading the environment
load_dotenv(dotenv_path=env_path_bench, override=True)
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
test_base_path = Path(USER_DATA) / args.test_base_path
dir_path(test_base_path)

glossary_file = Path(USER_DATA) / GLOSSARY_FILE
expression_file = Path(USER_DATA) / RAW_EXPRESSION_FILE
threshold_file = Path(USER_DATA) / THRESHOLD_FILE

test_base_df = pd.read_excel(test_base_path, engine="odf") #see if we take csv as input
#test_base_df = pd.read_csv(test_base_path, encoding= 'utf-8')




#Instanciation of elasticsearch
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])




import pdb; pdb.set_trace()
'''
#Index creation
for i in range(3): # to be sure alias and indexes are removed
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    es.indices.delete_alias(index='_all',
        name=INDEX_NAME, ignore=[400, 404])

create_index(INDEX_NAME, USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, RAW_EXPRESSION_FILE ) #some parameters are stored in the map, that is linked to the index here
#import pdb; pdb.set_trace()

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
#import pdb; pdb.set_trace()
'''
#Searching
rank_body = {}
rank_body_requests = []

must = {}
should = {}
filter = ''
highlight = []
for index, row in test_base_df.iterrows():

    must = [{"multi_match":{"fields":["question","reponse","titre","mots-cles"],"query":row['Questions']}}]
    body_built, length_of_request = build_query(must, should, filter, INDEX_NAME, highlight, glossary_file=glossary_file, expression_file=expression_file)
    body_query = body_built["query"] #removing highlight?

    request = { "id": index, "request": body_query, "ratings": [{ "_index": INDEX_NAME, "_id": row['Fiches'], "rating": 1}]}
    rank_body_requests.append(request)
    if index ==2:
        print('__________')
        print(request)
        print('__________')









#Saving



'''


D = es.rank_eval(body= {
  "requests": [
    {
      "id": "JFK query",
      "request": { "query": {
                    "bool": {
                        "must": [{"multi_match": { "query": "ministère"}}],
                        "filter": [],
                        "should": [],
                        "must_not": []
                                }
                        }},
      "ratings": [{ "_index": "bld_benchmark", "_id": "valorisation+données.odt", "rating": 1}]
    } ],
 
  "metric": {
    "dcg": {
      "k": 3,
      "normalize": False
    }
  }
}, index = INDEX_NAME )

doc = 'création+de+la+DNUM.odt'
req = 'DNUM'
must = [{"multi_match":{"fields":["question","reponse","titre","mots-cles"],"query":req}}]
time.sleep(1)
#import pdb; pdb.set_trace()
#D = es.search(index = INDEX_NAME, body = {'query':{'match_all':{}}}, size=10)

#print(es.get(index=INDEX_NAME, id='moteur de recherche.odt'))

res = search(must, [], [], INDEX_NAME, [],
              glossary_file = glossary_file,
              expression_file = expression_file,
              threshold_file = threshold_file)

print(res)

Brouillon
#Analyse
indices = elasticsearch.client.IndicesClient(es)
# Test synonym
res = indices.analyze(index = INDEX_NAME, body=body)
#Test  simple search
body = {
      "analyzer": "my_analyzer",
      "text": "La dnum du Ministère de l'interieur"
    }

D = es.search(index = INDEX_NAME,
                      body = body,
                      size = 10)

bod = { "query": {
                    "bool": {
                        "must": [{"multi_match": {"fields": ["question", "reponse", "titre", "mots-cles"], "query": "direction"}}],
                        "filter": [],
                        "should": [],
                        "must_not": []
                                }
                        },
            "highlight" : {
                "pre_tags" : ["<mark>"],
                "post_tags" : ["</mark>"],
                "fragment_size" : 300,
                "number_of_fragments" : 3,
                "order" : "score",
                "boundary_scanner" : "sentence",
                "boundary_scanner_locale" : "fr-FR",
                "fields":{}
                    }
                }


'''