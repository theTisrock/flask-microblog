# search

# flask
from flask import current_app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:  # __searchable__ is of type List
        # below builds a dictionary of attributes by
        # returning the values of the named attributes specified for that class's __searchable__ attrib.
        # it then stores the values of those attributes in the hashmap/dict.
        # could raise AttributeError
        payload[field] = getattr(model, field)  # reads the field item then scans the object for that attrib
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    if not current_app.elasticsearch:
        return
    search = current_app.elasticsearch.search(
        index=index,
        body={
            'query': { 'multi-match': {'query': query, 'fields': ['*']} },  # search all(*) fields
            'from': (page-1) * per_page,  # pagination
            'size': per_page
        }
    )
    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']

# end search
