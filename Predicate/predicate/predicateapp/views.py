from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response


def index(request):
    return render_to_response('index.html')


def login(request):
    return render_to_response('login.html')


def addDataset(request, challenge_id):
    return HttpResponse("<h1>challenge id " + str(challenge_id) + "</h1>")
