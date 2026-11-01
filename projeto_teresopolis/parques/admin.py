from django.contrib import admin

from .models import Parque


@admin.register(Parque)
class ParqueAdmin(admin.ModelAdmin):
    list_display = ["nome", "aberto", "horario_funcionamento", "atualizado_em"]
    list_filter = ["aberto"]
    prepopulated_fields = {"slug": ("nome",)}
