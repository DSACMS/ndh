from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Connection to ndh database: successful")

def health(request):
    return HttpResponse("healthy")
