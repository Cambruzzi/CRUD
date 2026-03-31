"""
Configuração Principal de URLs (Master Router) do Projeto.

Este arquivo funciona como a 'telefonista' da aplicação. Ele recebe todas as 
requisições HTTP da internet e as direciona (via 'include') para os arquivos 
urls.py específicos de cada aplicativo (ex: crud, usuários, etc.), ou para 
módulos globais como o Admin e a Documentação (Swagger).
"""

# 1. Imports do Django Core
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

# 2. Imports do Django REST Framework (Autenticação)
from rest_framework.authtoken import views as auth_views

# 3. Imports de Bibliotecas Terceirizadas (Swagger)
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


# =====================================================================
# VIEWS GLOBAIS
# =====================================================================
def tela_frontend(request):
    """
    View responsável por renderizar a Single Page Application (SPA) do frontend.
    
    Nota de Arquitetura: Em projetos muito grandes, esta view costuma ficar 
    dentro de um app dedicado chamado 'core' ou 'frontend'. Para o nosso 
    escopo atual, mantê-la aqui no roteador principal é perfeitamente funcional.
    """
    return render(request, 'index.html')


# =====================================================================
# REGISTRO DE ROTAS (URL PATTERNS)
# =====================================================================
urlpatterns = [
    # ---------------------------------------------------------
    # 1. ROTAS GLOBAIS E ADMINISTRAÇÃO
    # ---------------------------------------------------------
    path('admin/', admin.site.urls),
    
    path('', tela_frontend, name='tela_inicial'),

    # ---------------------------------------------------------
    # 2. ROTAS DA API REST (BACKEND)
    # ---------------------------------------------------------
    # CORREÇÃO CRÍTICA: Adicionada a barra final em 'api/'.
    # Isso garante que as rotas do app crud fiquem no formato: /api/v1/produtos/
    path('api/', include('crud.urls')),
    
    # Rota nativa do DRF para validar usuário e senha e devolver o Token
    path('api/login/', auth_views.obtain_auth_token, name='api_login'),

    # ---------------------------------------------------------
    # 3. DOCUMENTAÇÃO DA API (SWAGGER / OPENAPI)
    # ---------------------------------------------------------
    # Gera o arquivo invisível com o mapa da API (formato YAML/JSON)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    
    # Gera a interface visual (Tela Bonita) lendo o schema acima
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

# =====================================================================
# SERVIDOR DE MÍDIA (APENAS AMBIENTE DE DESENVOLVIMENTO)
# =====================================================================
if settings.DEBUG:
    """
    Libera o acesso HTTP para os arquivos que os usuários fizeram upload 
    (ex: fotos dos produtos). 
    Aviso: Em produção (DEBUG=False), o Nginx, Apache ou AWS S3 assumem esse papel.
    """
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)