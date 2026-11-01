from django.db import models


class Trilha(models.Model):
    class Dificuldade(models.TextChoices):
        BAIXA = "baixa", "Baixa"
        MEDIA = "media", "Média"
        ALTA = "alta", "Alta"

    parque = models.ForeignKey("parques.Parque", on_delete=models.CASCADE, related_name="trilhas")
    nome = models.CharField(max_length=150)
    dificuldade = models.CharField(max_length=10, choices=Dificuldade.choices, default=Dificuldade.MEDIA)
    duracao_estimada = models.CharField(max_length=40, help_text="Ex.: ~3h")
    descricao = models.TextField(blank=True)
    em_manutencao = models.BooleanField(default=False)

    class Meta:
        ordering = ["parque_id", "nome"]

    def __str__(self):
        return f"{self.nome} ({self.parque})"
