from django.db import models
from django.utils.text import slugify


class Parque(models.Model):
    nome = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    slogan = models.CharField("slogan (carrossel)", max_length=200, blank=True)
    descricao_curta = models.CharField("descrição curta (card da Home)", max_length=200, blank=True)
    sobre = models.TextField("sobre o parque", blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    horario_funcionamento = models.CharField(max_length=120, default="A confirmar")
    imagem_url = models.URLField(blank=True)
    aberto = models.BooleanField(default=True)
    mensagem_fechamento = models.TextField(
        blank=True, help_text="Exibida na faixa vermelha 'Parque Fechado'."
    )
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
