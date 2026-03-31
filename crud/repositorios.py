"""
Módulo de Repositório (Gateway / Data Access Layer).
Responsável exclusivo por realizar a comunicação com o Banco de Dados.
Isola o ORM do Django das regras de negócio (Camada de Services).
"""

from django.shortcuts import get_object_or_404
from django.db.models import QuerySet
from .models import Produto

def buscar_todos_os_produtos_no_banco() -> QuerySet[Produto]:
    return Produto.objects.all()


def buscar_produto_por_id(produto_id: int) -> Produto:
    return get_object_or_404(Produto, id=produto_id)


def salvar_produto(produto: Produto) -> Produto:
    # Se o produto não tem ID, ele faz um INSERT. Se já tem ID, ele faz um UPDATE.
    produto.save()
    return produto