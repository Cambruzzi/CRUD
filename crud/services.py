"""
Módulo de Serviços (Business Logic Layer).
Coração da aplicação. Contém todas as regras de negócio, validações complexas e
orquestração de chamadas.
"""

from typing import Dict, Any
from django.db.models import QuerySet
from .models import Produto
from . import repositorios

def listar_todos_produtos_ativos() -> QuerySet[Produto]:
    todos_produtos = repositorios.buscar_todos_os_produtos_no_banco()
    produtos_ativos = todos_produtos.filter(excluido=False)
    
    return produtos_ativos


def criar_novo_produto(dados_validados: Dict[str, Any]) -> Produto:
    novo_produto = Produto(
        nome=dados_validados.get('nome'),
        codigo=dados_validados.get('codigo'),
        valor=dados_validados.get('valor'),
        excluido=dados_validados.get('excluido', False),
        imagem=dados_validados.get('imagem')
    )
    return repositorios.salvar_produto(novo_produto)


def atualizar_produto(produto_id: int, dados_validados: Dict[str, Any]) -> Produto:
    """
    Busca um produto existente, aplica as alterações parciais permitidas e salva.
    
    Argumentos:
        produto_id (int): ID do produto a ser atualizado.
        dados_validados (dict): Dados novos fornecidos pelo cliente.
        
    Retorna:
        Produto: A instância atualizada.
    """
    # 1. Pede para o Gateway buscar o produto
    produto = repositorios.buscar_produto_por_id(produto_id)
    
    # 2. Aplica as atualizações apenas nos campos que vieram no dicionário
    produto.nome = dados_validados.get('nome', produto.nome)
    produto.codigo = dados_validados.get('codigo', produto.codigo)
    produto.valor = dados_validados.get('valor', produto.valor)
    produto.excluido = dados_validados.get('excluido', produto.excluido)
    
    # Tratamento especial para arquivos físicos (imagens)
    if 'imagem' in dados_validados:
        produto.imagem = dados_validados['imagem']
        
    # 3. Manda o Gateway salvar a alteração
    # Correção de Arquitetura: Removemos o produto.save() direto que estava aqui!
    return repositorios.salvar_produto(produto)


def deletar_produto(produto_id: int) -> Produto:
    """
    Aplica a regra de exclusão lógica (Soft Delete) em um produto.
    Em vez de apagar do banco, apenas inativa o registro para preservar histórico.
    
    Argumentos:
        produto_id (int): ID do produto a ser deletado.
        
    Retorna:
        Produto: A instância do produto com o status de excluído = True.
    """
    # 1. Pede para o Gateway buscar o produto
    produto = repositorios.buscar_produto_por_id(produto_id)
    
    # 2. Regra de Negócio Crítica: Exclusão Lógica
    produto.excluido = True
    
    # 3. Manda o Gateway persistir a mudança de estado
    return repositorios.salvar_produto(produto)