"""
Módulo de Roteamento (URL Dispatcher) do App.
Mapeia as URLs digitadas no navegador ou chamadas pelo Frontend 
para as suas respectivas Views e funções de controle.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

# Importação explícita das views para facilitar a leitura
from . import views, auth_views

urlpatterns = [
    # =====================================================================
    # ROTAS DA API REST (BACKEND / JSON) - Versão 1
    # =====================================================================
    # ⚠️ Padrão de Mercado: 
    # 1. Sem barra no começo (para não conflitar com o include principal).
    # 2. Sempre com barra no final (exigência do APPEND_SLASH do Django).
    
    # Autenticação
    path('v1/registrar/', auth_views.registrar_usuario_api, name='registrar_usuario_api'),
    
    # Produtos (Listagem e Criação)
    path('v1/produtos/', views.produto_api, name='produto_api'),
    
    # Produtos (Detalhe, Atualização e Deleção)
    # A tag <int:id> garante que a rota só aceite números inteiros, bloqueando textos acidentais.
    path('v1/produtos/<int:id>/', views.atualizar_produto_api, name='atualizar_produto_api'),
]

# =====================================================================
# CONFIGURAÇÃO DE ARQUIVOS ESTÁTICOS E MÍDIA (APENAS DESENVOLVIMENTO)
# =====================================================================
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)