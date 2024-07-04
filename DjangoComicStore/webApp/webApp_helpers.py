from store.models import comic
from django.core.cache import cache


def get_featured_cache():
    """
    Return dictionary of all elements in home page that are cached, if cache is not complete recaches all elements  
    """

    comic_featured_queryset = comic.objects.filter(featured = True)

    dict_to_cache = {
        "featured_comics":comic_featured_queryset,
    }

    if len(cache.get_many(dict_to_cache))!=dict_to_cache:
        cache.set_many(dict_to_cache,timeout=600)

    current_cache_dict = cache.get_many(dict_to_cache)
    
    return current_cache_dict