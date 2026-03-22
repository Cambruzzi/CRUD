from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def home_tarefas(request):
    return HttpResponse("<h1>Meu app de tarefas está vivo!</h1>")