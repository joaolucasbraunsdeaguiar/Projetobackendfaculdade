from django.utils import timezone
from rest_framework import serializers

from avisos.serializers import AvisoSerializer
from eventos.serializers import EventoSerializer
from trilhas.serializers import TrilhaSerializer

from .models import Parque


class ParqueSerializer(serializers.ModelSerializer):
    """Usado na listagem (carrossel e cards da Home) e nas escritas do ADM."""

    status = serializers.SerializerMethodField()
    horario_exibicao = serializers.SerializerMethodField()

    class Meta:
        model = Parque
        fields = [
            "id", "nome", "slug", "slogan", "descricao_curta", "sobre", "endereco",
            "horario_funcionamento", "horario_exibicao", "imagem_url",
            "aberto", "status", "mensagem_fechamento", "atualizado_em",
        ]
        read_only_fields = ["atualizado_em"]

    def get_status(self, obj):
        return "aberto" if obj.aberto else "fechado"

    def get_horario_exibicao(self, obj):
        return obj.horario_funcionamento if obj.aberto else "Fechado temporariamente"


class ParqueDetalheSerializer(ParqueSerializer):
    """Página de detalhes: info geral + trilhas + eventos + avisos."""

    trilhas = TrilhaSerializer(many=True, read_only=True)
    eventos = serializers.SerializerMethodField()
    avisos = serializers.SerializerMethodField()

    class Meta(ParqueSerializer.Meta):
        fields = ParqueSerializer.Meta.fields + ["trilhas", "eventos", "avisos"]

    def get_eventos(self, obj):
        proximos = obj.eventos.filter(data__gte=timezone.localdate())
        return EventoSerializer(proximos, many=True, context=self.context).data

    def get_avisos(self, obj):
        ativos = obj.avisos.filter(ativo=True)
        return AvisoSerializer(ativos, many=True, context=self.context).data


class ParqueStatusSerializer(serializers.ModelSerializer):
    """PATCH /api/parques/<id>/status/ : abre/fecha o parque."""

    class Meta:
        model = Parque
        fields = ["aberto", "mensagem_fechamento"]

    def validate(self, attrs):
        aberto = attrs.get("aberto", self.instance.aberto)
        if aberto:
            attrs["mensagem_fechamento"] = ""
        elif not attrs.get("mensagem_fechamento", self.instance.mensagem_fechamento):
            attrs["mensagem_fechamento"] = "Parque temporariamente fechado."
        return attrs
