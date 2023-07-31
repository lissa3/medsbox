from django.http import HttpResponse


def clear(request):
    """(htmx) help func to clean elem on htmx requests"""
    return HttpResponse("")
