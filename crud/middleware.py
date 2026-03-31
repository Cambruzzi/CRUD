"""
Módulo de Middlewares Globais da Aplicação.
Contém interceptadores que atuam na camada HTTP (antes do roteamento e das views).
"""

import time
import logging
from typing import Callable
# Imports do Django para Tipagem e Respostas
from django.http import HttpRequest, HttpResponse, JsonResponse
# Configuração do Logger (Padrão de mercado para substituir o 'print')
logger = logging.getLogger(__name__)


class InterceptadorMiddleware:
    """
    Middleware global de interceptação HTTP e Auditoria.
    
    Responsável por atuar como um 'porteiro' da aplicação (padrão Interceptor).
    Ele mede o tempo de resposta das requisições para fins de monitoramento de performance (APM)
    e aplica filtros globais de segurança antes que a requisição alcance a camada de Negócios.
    """

    def __init__(self, get_response: Callable):
        """
        Configuração inicial do middleware. 
        Este método é executado apenas uma vez, no momento em que o servidor web inicia.
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """
        (Onion Architecture), interceptando o 
        fluxo de entrada (request) e o fluxo de saída (response).
        """
        # Log de auditoria: Registra quem está tentando acessar o quê
        logger.info(f"🚪 Requisição Inbound: [{request.method}] {request.path}")
        
        # Inicia o cronômetro para medir a saúde e velocidade da API
        tempo_inicial = time.time()

        # Regra de Segurança Global (Firewall de Aplicação Básico):
        # Bloqueia rotas restritas logo na entrada, poupando processamento de Views e Banco de Dados.
        if "secreto" in request.path:
            logger.warning(f"🔒 Segurança: Tentativa de acesso bloqueada na rota restrita: {request.path}")
            return JsonResponse({"erro": "Acesso negado. Privilégios insuficientes."}, status=403)

        response = self.get_response(request)

        # Calcula o tempo total gasto para processar a requisição e gerar a resposta
        tempo_total = time.time() - tempo_inicial
        
        # Observabilidade: Registra quanto tempo o servidor demorou para processar o ciclo completo
        logger.info(f"⏱️ Requisição Outbound: {request.path} processada em {tempo_total:.4f} segundos.")

        # Finalmente, entrega a caixa (Response) na mão do carteiro (Navegador/Frontend)
        return response