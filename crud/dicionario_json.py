"""
Módulo de Serializadores da API de Produtos.
Responsável por converter objetos complexos do banco de dados (Models) em tipos de dados 
nativos do Python (que serão renderizados em JSON para a web) e vice-versa.
"""

from rest_framework import serializers
from .models import Produto

class ProdutosDicionario(serializers.ModelSerializer):
    """
    Serializador principal para o modelo Produto.
    
    Herda de 'ModelSerializer' para automatizar a criação dos campos baseados no banco de dados,
    garantindo que as regras (como max_length ou blank=True) definidas no Model sejam 
    aplicadas automaticamente na validação da API.
    """

    class Meta:
        model = Produto
        fields = [
            'id', 
            'nome', 
            'codigo', 
            'valor', 
            'excluido', 
            'data_alteracao',
            'imagem'
        ]
        read_only_fields = ['id', 'data_alteracao']