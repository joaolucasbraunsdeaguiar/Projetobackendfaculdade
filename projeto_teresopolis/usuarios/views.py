from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import LoginSerializer, UsuarioSerializer


class LoginView(APIView):
    """POST /api/auth/login/ -> {"email": "...", "senha": "..."} devolve o token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        dados = LoginSerializer(data=request.data)
        dados.is_valid(raise_exception=True)

        candidato = User.objects.filter(email__iexact=dados.validated_data["email"]).first()
        user = None
        if candidato:
            user = authenticate(
                request=request,
                username=candidato.username,
                password=dados.validated_data["senha"],
            )

        if user is None or not user.is_staff:
            return Response(
                {"detail": "E-mail ou senha inválidos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "usuario": UsuarioSerializer(user).data})


class LogoutView(APIView):
    """POST /api/auth/logout/ (botão "Sair" do painel) invalida o token."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """GET /api/auth/me/ devolve o funcionário logado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UsuarioSerializer(request.user).data)
