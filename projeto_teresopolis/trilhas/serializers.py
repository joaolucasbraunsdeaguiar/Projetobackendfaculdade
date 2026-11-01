from rest_framework import serializers

from .models import Trilha


class TrilhaSerializer(serializers.ModelSerializer):
    dificuldade_display = serializers.CharField(source="get_dificuldade_display", read_only=True)

    class Meta:
        model = Trilha
        fields = [
            "id", "parque", "nome", "dificuldade", "dificuldade_display",
            "duracao_estimada", "descricao", "em_manutencao",
        ]
