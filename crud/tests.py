from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .models import Produto
from django.urls import reverse

class TesteProdutoAPI(APITestCase):    
    def setUp(self):
        self.usuario = User.objects.create_user(username='tester', password='123')
        self.client.force_authenticate(user=self.usuario)
        self.url_produtos = reverse('produto_api')
    def test_cadastrar_produto_com_sucesso(self):
        dados = {
            'nome': 'Notebook Teste',
            'codigo': '12345',
            'valor': 2500.00
        }        
        resposta = self.client.post(self.url_produtos, dados, format='json')        
        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertEqual(Produto.objects.get().nome, 'Notebook Teste')
    def test_bloquear_cadastro_sem_login(self):
        self.client.logout()
        dados = {'nome': 'Hacker', 'codigo': '666', 'valor': 0}        
        resposta = self.client.post(self.url_produtos, dados, format='json')        
        self.assertEqual(resposta.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Produto.objects.count(), 0)