#!/usr/bin/env python

import sys
import simplejson as json
import logging
import sys, os
import pprint
import argparse
from itertools import islice
from elasticsearch import Elasticsearch, helpers

def connect_elasticsearch():
    es = None
    es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
    # if es.ping():
        # print('Connected ElasticSearch')
    # else:
        # print('Failed Connect ElasticSearch!')
    return es

def create_index(es_object, index_name):
    created = False
    # index settings
    settings = {
        "mappings": {
            "news":{
                "properties":{ 
                    "id" : {"type":"text"},
                    "html": {"type":"text"}, 
                    "title": {"type": "text"}, 
                    "time":{"type":"text"}, 
                    "short_content": {"type": "text"}, 
                    "full_content": {"type": "text"}
                }
            }
        }
    }

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            # print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created

def load_json(index_name, directory):
    op_list = []
    # Get all file json in directory
    for filename in os.listdir(directory):
        if filename.endswith('.json'):
            i = 0
            with open(os.path.join(directory, filename),'r') as open_file:
                for record in open_file:
                    if(i%2 == 0):
                        id = record[20:-2]
                    else:
                        op_list.append({
                            '_index': index_name,
                            '_type' : 'news',
                            '_id': id,
                            '_source': record
                        })
                    i += 1
    # print("Imported records to index!")
    return op_list

def convert(obj):
    if isinstance(obj, bool):
        return str(obj).lower()
    if isinstance(obj, (list, tuple)):
        return [convert(item) for item in obj]
    if isinstance(obj, dict):
        return {convert(key):convert(value) for key, value in obj.items()}
    return obj

def search(es_object, index_name, search):
    res = es.search(index=index_name, body=search)
    print(json.dumps(res))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Elastic Search')
    parser.add_argument('-i', '--index_name', type=str, required=True, help='Index Name')
    parser.add_argument('-l', '--load_data', type=str, help='Create and load data by import json file to index - yes')
    parser.add_argument('-s', '--search', type=str, help='Search query. - query')
    args = parser.parse_args()

    # Check ES Connection
    es = connect_elasticsearch()
    logging.basicConfig(level=logging.ERROR)
    if args.load_data == 'yes':
        if es is not None:
        # Create index if dont have
            if create_index(es, args.index_name):
                #Import data to index in ES
                helpers.bulk(client=es, actions=load_json(args.index_name, os.path.join(os.path.dirname(__file__), '../json_file2/')))
    
    if (args.search) and (es is not None):
        search_object = {"query": {"multi_match": {"query":args.search, "fields": [ "title", "short_content", "full_content" ]}}}
        search(es, args.index_name, json.dumps(search_object))