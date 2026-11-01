from django.contrib import admin

from .models import Aviso


@admin.register(Aviso)
class AvisoAdmin(admin.ModelAdmin):
    list_display = ["parque", "tipo", "titulo", "ativo", "criado_em"]
    list_filter = ["parque", "tipo", "ativo"]
