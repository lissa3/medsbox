from django.contrib.postgres.search import SearchQuery
from django.http import HttpResponse

from src.posts.models.post_model import Post


def clear(request):
    """(htmx) help func to clean elem on htmx requests"""
    return HttpResponse("")


def make_query(current_lang, user_inp):
    """
    separated query config;
    (no postgres config for uk to make a trigger)
    """
    lang_dict = {"en": "english", "ru": "russian", "nl": "dutch"}
    if current_lang != "uk":
        query = SearchQuery(
            user_inp, config=lang_dict[current_lang], search_type="websearch"
        )
    else:
        query = user_inp
    return query


def search_qs(current_lang, query):
    """
    split diff lang for search
    """
    if current_lang == "uk":
        posts = Post.objects.search_uk(query_text=query)
    elif current_lang == "en":
        posts = Post.objects.get_public().filter(vector_en=query)
    elif current_lang == "ru":
        posts = Post.objects.get_public().filter(vector_ru=query)

    return posts
