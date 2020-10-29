import argparse
import pytest
import json, os, time
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from tools.elastic import get_index_name, replace_blue_green, create_index, put_alias, inject_documents, search, index_file, suggest
import elasticsearch
from elasticsearch import Elasticsearch


'''Getting the arguments
- the path of the Q/A test base
- the list of the metrics
- the path of the environment (ex: bld/.env-bld)
backend/benchmark/bld/.env-bld
'''
parser = argparse.ArgumentParser(description='Evaluation of the metrics')
parser.add_argument('env_path', metavar='path',type=str,help='the path to env file')
args = parser.parse_args()
print(args)
print(args.env_path)

#Loading the environment
#env_path_bench = '/app/benchmark/' + args.env_path
env_path_bench = '/app/benchmark/bld/.env-bld' 
print(os.path.exists(env_path_bench))


load_dotenv(dotenv_path=env_path_bench)

INDEX_NAME = os.getenv('INDEX_NAME')
print(INDEX_NAME)
import pdb; pdb.set_trace()

USER_DATA = os.getenv('USER_DATA')
ES_DATA = os.getenv('ES_DATA')

GLOSSARY_FILE = os.getenv('GLOSSARY_FILE')
RAW_EXPRESSION_FILE = os.getenv('RAW_EXPRESSION_FILE')
MAPPING_FILE =  os.getenv('MAPPING_FILE')


PDF_DIR = os.getenv('PDF_DIR')
DST_DIR = os.getenv('DST_DIR')
JSON_DIR = os.getenv('JSON_DIR')
META_DIR =  os.getenv('META_DIR')

ES_PORT=os.getenv('ES_PORT')
ES_HOST=os.getenv('ES_HOST')


#Instanciation of elasticsearch
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])

#Index creation
for i in range(3): # to be sure alias and indexes are removed
    es.indices.delete(index=INDEX_NAME, ignore=[400, 404])
    es.indices.delete_alias(index='_all',
        name=INDEX_NAME, ignore=[400, 404])

create_index(INDEX_NAME, USER_DATA, ES_DATA, MAPPING_FILE, GLOSSARY_FILE, RAW_EXPRESSION_FILE )

#Injection of documents
inject_documents(INDEX_NAME, USER_DATA, DST_DIR, JSON_DIR,
                meta_path = META_DIR)

#Searching
D = es.search(index = INDEX_NAME,
                      body = body,
                      size = 10)
'''
res = es.get(index=INDEX_NAME, id='BF2014-18-14082 - CVAE.pdf')
.search(
    index="my-index",
    body={
      "query": {
        "filtered": {
          "query": {
            "bool": {
              "must": [{"match": {"title": "python"}}],
              "must_not": [{"match": {"description": "beta"}}]
            }
          },
          "filter": {"term": {"category": "search"}}
        }
      },
      "aggs" : {
        "per_tag": {
          "terms": {"field": "tags"},
          "aggs": {
            "max_lines": {"max": {"field": "lines"}}
          }
        }
      }
    }
)
'''


'''

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process command line arguments.')
    parser.add_argument('env_path', metavar='path',type=str,help='the path to env file')
    args = parser.parse_args()
    input_path = parser.parse_args()
    
    if not os.path.isfile(input_path):
        print('The path specified does not exist')
        sys.exit()

    print('voilà')
    print(args.env_path)
    return parser.parse_args

def dir_path(path):
    if path.exists():
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")



parse_arguments()'''