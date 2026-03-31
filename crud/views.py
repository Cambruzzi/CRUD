"""
Módulo de Views (Controllers / Presentation Layer).
Responsável por receber as requisições HTTP, delegar as validações de dados para os Serializers,
acionar as regras de negócio nos Services e retornar as respostas HTTP (JSON).
"""

# 1. Imports do Django
from django.http import HttpResponse

# 2. Imports do Django REST Framework (DRF)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 3. Imports do Swagger / Documentação
from drf_spectacular.utils import extend_schema

# 4. Imports Locais (Arquitetura Interna)
from .dicionario_json import ProdutosDicionario  # Nome atualizado para o padrão de mercado!
from . import services

# =====================================================================
# ROTAS DA API REST (BACKEND)
# =====================================================================

# Documentação específica para o método POST
@extend_schema(
    methods=['POST'],
    summary="Cadastrar um novo produto",
    description="Cria um produto. ⚠️ **Requer Token Bearer**.",
    request=ProdutosDicionario,
    responses={201: ProdutosDicionario, 400: None},
    tags=["Produtos"]
)
# Documentação específica para o método GET
@extend_schema(
    methods=['GET'],
    summary="Listar produtos ativos",
    description="Retorna a lista de todos os produtos que não foram excluídos logicamente.",
    responses={200: ProdutosDicionario(many=True)},
    tags=["Produtos"]
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def produto_api(request):
    """
    Endpoint (Collection) para listagem e criação de produtos.
    """
    # ---------------------------------------------------------
    # MÉTODO GET: Buscar e Listar
    # ---------------------------------------------------------
    if request.method == 'GET':
        # 1. Busca os dados puros no Service
        produtos = services.listar_todos_produtos_ativos()
        
        # 2. Transforma (Serializa) os objetos complexos em Dicionários/JSON
        # many=True avisa que é uma lista com vários itens, não apenas um.
        serializer = ProdutosDicionario(produtos, many=True)
 
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # ---------------------------------------------------------
    # MÉTODO POST: Receber e Criar
    # ---------------------------------------------------------
    elif request.method == 'POST':
        # 1. Joga os dados que vieram do Frontend dentro do molde do Serializer
        serializer = ProdutosDicionario(data=request.data)
        
        # 2. Verifica se os tipos de dados estão corretos (ex: valor é número?)
        if serializer.is_valid():
            # 3. Manda os dados limpos para a Regra de Negócio criar e salvar
            novo_produto = services.criar_novo_produto(serializer.validated_data)
            
            resposta_serializer = ProdutosDicionario(novo_produto)
            return Response(resposta_serializer.data, status=status.HTTP_201_CREATED)
            
        # Se a validação falhar, devolve exatamente qual campo deu erro
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Documentação específica para o método PUT
@extend_schema(
    methods=['PUT'],
    summary="Atualizar produto (Parcial)",
    description="Atualiza dados de um produto existente via ID.",
    request=ProdutosDicionario,
    responses={200: ProdutosDicionario, 400: None},
    tags=["Produtos"]
)
# Documentação específica para o método DELETE
@extend_schema(
    methods=['DELETE'],
    summary="Deletar produto (Soft Delete)",
    description="Oculta o produto do sistema sem apagá-lo do banco de dados.",
    responses={204: None},
    tags=["Produtos"]
)
@api_view(['PUT', 'DELETE'])
def atualizar_produto_api(request, id):
    """
    Endpoint (Detail) para alterar ou excluir um produto específico.
    """
    # ---------------------------------------------------------
    # MÉTODO PUT: Atualização
    # ---------------------------------------------------------
    if request.method == 'PUT':
        serializer = ProdutosDicionario(data=request.data, partial=True)
        
        if serializer.is_valid():
            produto_atualizado = services.atualizar_produto(id, serializer.validated_data)
            
            resposta_serializer = ProdutosDicionario(produto_atualizado)
            return Response(resposta_serializer.data, status=status.HTTP_200_OK)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # ---------------------------------------------------------
    # MÉTODO DELETE: Exclusão Lógica
    # ---------------------------------------------------------
    elif request.method == 'DELETE':
        services.deletar_produto(id)
        return Response(status=status.HTTP_204_NO_CONTENT)