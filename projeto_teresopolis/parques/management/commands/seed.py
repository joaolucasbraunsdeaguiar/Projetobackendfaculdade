from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from avisos.models import Aviso
from eventos.models import Evento
from parques.models import Parque
from trilhas.models import Trilha


class Command(BaseCommand):
    help = "Popula o banco com os 3 parques de Teresópolis (dados do protótipo) e um usuário ADM."

    def handle(self, *args, **options):
        serra, _ = Parque.objects.update_or_create(
            slug="parque-nacional-da-serra-dos-orgaos",
            defaults=dict(
                nome="Parque Nacional da Serra dos Órgãos",
                slogan="Beleza, aventura e preservação em um só lugar.",
                descricao_curta="Montanhas, trilhas e paisagens incríveis.",
                sobre=(
                    "O PARNASO é uma das unidades de conservação mais importantes do país, "
                    "com paisagens deslumbrantes e rica biodiversidade."
                ),
                endereco="Estrada Teresópolis-Friburgo, km 22",
                horario_funcionamento="A confirmar",
                aberto=False,
                mensagem_fechamento=(
                    "Devido a condições climáticas adversas, o parque permanecerá fechado até novo aviso."
                ),
            ),
        )
        tres_picos, _ = Parque.objects.update_or_create(
            slug="parque-estadual-dos-tres-picos",
            defaults=dict(
                nome="Parque Estadual dos Três Picos",
                slogan="Natureza preservada e desafios para todos.",
                descricao_curta="Natureza preservada e desafios para todos.",
                endereco="A confirmar",
                horario_funcionamento="A confirmar",
                aberto=True,
            ),
        )
        montanhas, _ = Parque.objects.update_or_create(
            slug="parque-natural-municipal-montanhas-de-teresopolis",
            defaults=dict(
                nome="Parque Natural Municipal Montanhas de Teresópolis",
                slogan="Um refúgio verde no coração da cidade.",
                descricao_curta="Um refúgio verde no coração da cidade.",
                endereco="Teresópolis - RJ",
                horario_funcionamento="A confirmar",
                aberto=True,
            ),
        )

        Trilha.objects.get_or_create(
            parque=serra, nome="Travessia Petrópolis-Teresópolis",
            defaults=dict(dificuldade="alta", duracao_estimada="~6h"),
        )
        Trilha.objects.get_or_create(
            parque=serra, nome="Caminho do Sino",
            defaults=dict(dificuldade="media", duracao_estimada="~3h"),
        )
        dedo, _ = Trilha.objects.get_or_create(
            parque=serra, nome="Trilha do Dedo de Deus",
            defaults=dict(dificuldade="alta", duracao_estimada="~4h", em_manutencao=True),
        )
        Aviso.objects.get_or_create(
            parque=serra, trilha=dedo, tipo="manutencao",
            defaults=dict(mensagem="Algumas trilhas estão em manutenção (como a Trilha do Dedo de Deus)."),
        )

        Evento.objects.get_or_create(
            parque=serra, titulo="Trilha Guiada no PARNASO", data=date(2026, 11, 25),
            defaults=dict(descricao="Uma experiência única com guias especializados."),
        )
        Evento.objects.get_or_create(
            parque=tres_picos, titulo="Observação de Aves nos Três Picos", data=date(2026, 11, 15),
            defaults=dict(descricao="Descubra a rica fauna da nossa região."),
        )

        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                "admin", "admin@teresopolis.rj.gov.br", "admin12345",
                first_name="Gestor", last_name="Parques",
            )
            self.stdout.write("Usuário ADM criado: admin@teresopolis.rj.gov.br / admin12345")

        self.stdout.write(self.style.SUCCESS("Banco populado."))
