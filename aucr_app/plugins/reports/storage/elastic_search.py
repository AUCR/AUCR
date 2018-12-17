# coding=utf-8
import os
from multiprocessing import Process
from flask import current_app
from elasticsearch import Elasticsearch


def index_data_to_es(index, payload):
    try:
        if current_app:
            current_app.elasticsearch.index(index=index, doc_type=index, id=None, body=payload, request_timeout=120)
        else:
            es = Elasticsearch(os.environ.get("ELASTICSEARCH_URL"))
            es.index(index=index, doc_type=index, id=None, body=payload, request_timeout=120)

    except AttributeError:
        pass


def index_model_data_to_es(index, model):
    payload = {}
    try:
        if model.__searchable__:
            for field in model.__searchable__:
                payload[field] = getattr(model, field)
            current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload, request_timeout=120)
    except AttributeError:
        pass


def add_model_to_index(index, model):
    """Ad to Elasticsearch index."""
    if not current_app.elasticsearch:
        return
    p = Process(target=index_model_data_to_es, args=(index, model))
    p.start()


def add_to_index(index, payload):
    """Ad to Elasticsearch index."""
    if not current_app.elasticsearch:
        return
    p = Process(target=index_data_to_es, args=(index, payload))
    p.start()


def remove_from_index(index, model):
    """Elasticsearch remove field from index."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id, request_timeout=120)


def query_index(index, query, page, per_page):
    """Elasticsearch query field from index."""
    if current_app:
        if index == "message":
            search = current_app.elasticsearch.search(
                index=index, doc_type=index,
                body={"query": {"match": {'body': query}}}, request_timeout=120)
            ids = [int(hit['_id']) for hit in search['hits']['hits']]
        else:
            search = current_app.elasticsearch.search(
                index=index, doc_type=index,
                body={"query": {"multi_match": {"query": query, "type":  "best_fields"}}},
                request_timeout=120)
            ids = [int(hit['_id']) for hit in search['hits']['hits']]

        return ids, search['hits']['total']
    else:
        try:
            es = Elasticsearch(os.environ.get("ELASTICSEARCH_URL"))
            search = es.search(
                index=index, doc_type=index,
                body={"query": {"match_all": {}}}, request_timeout=120)
            ids = [(hit['id']) for hit in search['hits']['hits']]
            return ids, search['hits']['total']
        except:
            if not current_app.elasticsearch:
                return [], 0
