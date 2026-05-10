from django.contrib.auth import authenticate
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Usuario, Perfil

from .serializers import (
    LoginSerializer,
    UsuarioSerializer,
    PerfilSerializer,
    CriarUsuarioSerializer
)

class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_excepetion=True
        )

        usuario = authenticate(
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if not usuario:
            return Response(
                {'erro': 'Credenciais Inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(
            usuario
        )

        return Response({
            'acess': str(refresh.acess_token),
            'refresh': str(refresh),
            'usuario': UsuarioSerializer(usuario).data
        })

class MeView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def get(self, request):

        serializer = UsuarioSerializer(
            request.user
        )

        return Response(
            serializer.data
        )

class UsuarioViewSet(
    viewsets.ModelViewSet
):

    queryset = Usuario.objects.all()

    def get_serializer_class(self):

        if self.action == 'create':
            return CriarUsuarioSerializer

        return UsuarioSerializer

class PerfilViewSet(
    viewsets.ModelViewSet
):

    queryset = Perfil.objects.all()

    serializer_class = PerfilSerializer