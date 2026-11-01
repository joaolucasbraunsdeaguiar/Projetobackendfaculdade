from django.db import models


class Evento(models.Model):
    parque = models.ForeignKey("parques.Parque", on_delete=models.CASCADE, related_name="eventos")
    titulo = models.CharField(max_length=150)
    data = models.DateField()
    descricao = models.TextField(blank=True)
    imagem_url = models.URLField(blank=True)

    class Meta:
        ordering = ["data", "titulo"]

    def __str__(self):
        return f"{self.titulo} - {self.data:%d/%m/%Y}"
