from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def home(request: HttpRequest) -> HttpResponse:
    ctx = {}
    return render(request, "core/home.html", ctx)


def intro(request: HttpRequest) -> HttpResponse:
    ctx = {}
    return render(request, "core/intro.html", ctx)
