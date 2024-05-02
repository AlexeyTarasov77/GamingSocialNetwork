from algoliasearch_django import algolia_engine

def get_client():
    return algolia_engine.client

def get_index(index_name):
    return get_client().init_index(index_name)

def perform_search(index_name, query, **kwargs):
    index = get_index(index_name)
    assert index is not None, f"Index {index_name} not found"
    params = {}
    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        params["tagFilters"] = tags
    index_filters = [f"{key}:{value}" for key, value in kwargs.items() if value] or []
    params["facetFilters"] = index_filters
    return index.search(query, params)