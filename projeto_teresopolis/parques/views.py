from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Parque
from .serializers import (
    ParqueDetalheSerializer,
    ParqueSerializer,
    ParqueStatusSerializer,
)


class ParqueViewSet(viewsets.ModelViewSet):
    queryset = Parque.objects.all()

    def get_queryset(self):
        qs = super().get_queryset()
        if self.action == "retrieve":
            qs = qs.prefetch_related("trilhas", "eventos", "avisos")
        return qs

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ParqueDetalheSerializer
        if self.action == "alterar_status":
            return ParqueStatusSerializer
        return ParqueSerializer

    @action(detail=True, methods=["patch"], url_path="status", url_name="status")
    def alterar_status(self, request, pk=None):
        parque = self.get_object()
        serializer = self.get_serializer(parque, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(ParqueDetalheSerializer(parque, context={"request": request}).data)


class ContatoView(APIView):
    """GET /api/contato/ : dados da tela Contatos."""

    permission_classes = [AllowAny]

    def get(self, request):
        return Response(settings.CONTATO)
