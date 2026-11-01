from django.db import models


class Aviso(models.Model):
    class Tipo(models.TextChoices):
        MANUTENCAO = "manutencao", "Manutenção de trilha"
        INTERDICAO = "interdicao", "Interdição"
        GERAL = "geral", "Aviso geral"

    parque = models.ForeignKey("parques.Parque", on_delete=models.CASCADE, related_name="avisos")
    trilha = models.ForeignKey(
        "trilhas.Trilha", on_delete=models.SET_NULL, null=True, blank=True, related_name="avisos"
    )
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.GERAL)
    titulo = models.CharField(max_length=150, blank=True)
    mensagem = models.TextField()
    ativo = models.BooleanField(default=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.parque}"
