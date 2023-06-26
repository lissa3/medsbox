from django.shortcuts import render


def home(request):
    return render(request, "home.html")


def intro(request):
    return render(request, "intro.html")
