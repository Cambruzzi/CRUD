from django.urls import path
from . import views

urlpatterns = [
    # Quando o usuário acessar a rota vazia do app, chama a view home_tarefas
    path('', views.home_tarefas, name='home'), 
]