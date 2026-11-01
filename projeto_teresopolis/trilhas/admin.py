from django.contrib import admin

from .models import Trilha


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ["nome", "parque", "dificuldade", "duracao_estimada", "em_manutencao"]
    list_filter = ["parque", "dificuldade", "em_manutencao"]
