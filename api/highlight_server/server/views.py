from django.shortcuts import render
import json
# Create your views here.

from django.http import HttpResponse
from . import registration as rg


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request):
    result = {'id': 120}
    if request.method == "GET":
        params = request.GET

        login1 = params["login"]
        pwd = params["password"]
        # user_type = params["type"]
        result = rg.log_in(login1, pwd)


    text = json.dumps(result)
    return HttpResponse(text)

