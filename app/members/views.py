from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    print "hit index."
    return HttpResponse("Hello, cruel world. YO. nah bro.")