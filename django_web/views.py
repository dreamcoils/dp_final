from django.shortcuts import render
from es_module import es_query
from graph_recommend import recommend

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello Django')


def es(request):
    res = es_query.query(request.GET.get("q"))
    return HttpResponse(res)


def graph_rec(request):
    user_id = request.GET.get("user_id")
    PATH = "graph_recommend/features/kgcn_features.pth"
    res = recommend.rec_foods(user_id, PATH)
    return HttpResponse(res)
