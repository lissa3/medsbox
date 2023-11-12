from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from src.posts.models.media_model import Video


def home(request: HttpRequest) -> HttpResponse:
    ctx = {"vidos": Video.objects.last()}
    return render(request, "core/home.html", ctx)


def intro(request: HttpRequest) -> HttpResponse:
    ctx = {}
    return render(request, "core/intro.html", ctx)
