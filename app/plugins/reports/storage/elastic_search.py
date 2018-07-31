# coding=utf-8
from multiprocessing import Process
from flask import current_app


def index_model_data_to_es(index, model):
    payload = {}
    try:
        if model.__searchable__:
            for field in model.__searchable__:
                payload[field] = getattr(model, field)
            current_app.elasticsearch.index(index=index, doc_type=index, id=model.id, body=payload)
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
    current_app.elasticsearch.index(index=index, doc_type=index, body=payload)


def remove_from_index(index, model):
    """Elasticsearch remove field from index."""
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page):
    """Elasticsearch query field from index."""
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, doc_type=index,
        body={'query': query, 'fields': ['*']})
    ids = [int(hit['id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
