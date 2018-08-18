import os
from elasticsearch import Elasticsearch

es = Elasticsearch()

index_name = 'play_history'

def index_track(track, doc_id):
    res = es.index(index=index_name, body=track, id=doc_id, doc_type='_doc')    
    es.indices.refresh()
    return res

def track_exists(doc_id):
    if not es.indices.exists(index_name):
        return False
    result = es.get(index=index_name, id=doc_id, doc_type='_doc', ignore=[404])
    return result['found']