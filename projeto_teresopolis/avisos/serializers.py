from rest_framework import serializers

from .models import Aviso


class AvisoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aviso
        fields = ["id", "parque", "trilha", "tipo", "titulo", "mensagem", "ativo", "criado_em"]
        read_only_fields = ["criado_em"]

    def validate(self, attrs):
        parque = attrs.get("parque", getattr(self.instance, "parque", None))
        trilha = attrs.get("trilha", getattr(self.instance, "trilha", None))
        if trilha and parque and trilha.parque_id != parque.id:
            raise serializers.ValidationError({"trilha": "Essa trilha não pertence ao parque informado."})
        return attrs
