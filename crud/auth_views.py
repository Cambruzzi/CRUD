"""
Módulo de Autenticação da API.
Responsável por gerenciar endpoints de registro, login e tokens de acesso.
"""
# 1. Imports do Django
from django.contrib.auth.models import User
# 2. Imports do Django REST Framework (DRF)
from rest_framework import status, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
# 3. Imports de Bibliotecas Terceirizadas (Swagger/OpenAPI)
from drf_spectacular.utils import extend_schema, inline_serializer
@extend_schema(
    summary="Registrar novo usuário",
    description="Cria uma nova conta de usuário, aplica o hash seguro na senha e retorna um Token de acesso Bearer.",
    tags=["Autenticação"], # Agrupa este endpoint na aba "Autenticação" do Swagger
    request=inline_serializer(
        name="RegistroUsuarioRequest",
        fields={
            "username": serializers.CharField(required=True),
            "password": serializers.CharField(
                required=True, 
                style={'input_type': 'password'} # Mascara o input na interface da documentação
            ),
        }
    ),
    responses={
        201: inline_serializer(
            name="RegistroUsuarioResponse",
            fields={
                "mensagem": serializers.CharField(),
                "token": serializers.CharField(),
            }
        ),
        400: inline_serializer(
            name="ErroValidacaoResponse",
            fields={"erro": serializers.CharField()}
        )
    }
)
@api_view(['POST'])
@permission_classes([AllowAny]) # Permite acesso público (não exige token para criar a conta)
def registrar_usuario_api(request):
    """
    Recebe credenciais via POST, valida regras de negócio (dados vazios e duplicidade),
    cria um usuário no banco de dados e gera seu respectivo token de autenticação.
    """
    username = request.data.get('username')
    password = request.data.get('password')

    # Validação de dados obrigatórios
    if not username or not password:
        return Response(
            {"erro": "Dados inválidos. Os campos 'username' e 'password' são obrigatórios."}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Regra de negócio: Previne a criação de contas com o mesmo nome de usuário
    if User.objects.filter(username=username).exists():
        return Response(
            {"erro": "Não foi possível realizar o cadastro. Este nome de usuário já está em uso."}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    # Persistência: Utilizamos 'create_user' para garantir que a senha seja salva com Hash irreversível (PBKDF2)
    novo_usuario = User.objects.create_user(username=username, password=password)
    
    # Gera o token de acesso exclusivo e permanente para a nova conta
    token = Token.objects.create(user=novo_usuario)

    return Response(
        {
            "mensagem": "Usuário criado com sucesso!",
            "token": token.key
        }, 
        status=status.HTTP_201_CREATED
    )