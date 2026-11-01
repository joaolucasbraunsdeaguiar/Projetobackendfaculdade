from datetime import timedelta

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from avisos.models import Aviso
from eventos.models import Evento
from parques.models import Parque
from trilhas.models import Trilha


class ApiParquesTests(APITestCase):
    def setUp(self):
        self.parque = Parque.objects.create(nome="Parque Teste", descricao_curta="Curta")
        self.admin = User.objects.create_user("admin", "admin@x.com", "senha12345", is_staff=True)
        self.comum = User.objects.create_user("comum", "comum@x.com", "senha12345")

    # ---- área pública ----
    def test_listagem_publica(self):
        resp = self.client.get("/api/parques/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data[0]["nome"], "Parque Teste")
        self.assertEqual(resp.data[0]["slug"], "parque-teste")

    def test_detalhe_traz_trilhas_eventos_e_avisos(self):
        trilha = Trilha.objects.create(
            parque=self.parque, nome="Trilha A", dificuldade="alta",
            duracao_estimada="~6h", em_manutencao=True,
        )
        hoje = timezone.localdate()
        Evento.objects.create(parque=self.parque, titulo="Futuro", data=hoje + timedelta(days=5))
        Evento.objects.create(parque=self.parque, titulo="Passado", data=hoje - timedelta(days=5))
        Aviso.objects.create(parque=self.parque, trilha=trilha, tipo="manutencao", mensagem="Em obras")
        Aviso.objects.create(parque=self.parque, mensagem="Antigo", ativo=False)

        resp = self.client.get(f"/api/parques/{self.parque.id}/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.data["trilhas"]), 1)
        self.assertEqual([e["titulo"] for e in resp.data["eventos"]], ["Futuro"])
        self.assertEqual(len(resp.data["avisos"]), 1)

    def test_publico_nao_ve_aviso_inativo(self):
        Aviso.objects.create(parque=self.parque, mensagem="Antigo", ativo=False)
        self.assertEqual(len(self.client.get("/api/avisos/").data), 0)

    # ---- permissões ----
    def test_anonimo_nao_cria_parque(self):
        resp = self.client.post("/api/parques/", {"nome": "Novo"})
        self.assertEqual(resp.status_code, 401)

    def test_usuario_sem_is_staff_nao_cria_parque(self):
        self.client.force_authenticate(self.comum)
        resp = self.client.post("/api/parques/", {"nome": "Novo"})
        self.assertEqual(resp.status_code, 403)

    def test_admin_cria_parque(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.post("/api/parques/", {"nome": "Novo Parque"})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data["slug"], "novo-parque")

    # ---- status aberto/fechado ----
    def test_admin_fecha_e_reabre_parque(self):
        self.client.force_authenticate(self.admin)
        url = f"/api/parques/{self.parque.id}/status/"

        resp = self.client.patch(url, {"aberto": False, "mensagem_fechamento": "Chuva forte"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["status"], "fechado")
        self.assertEqual(resp.data["horario_exibicao"], "Fechado temporariamente")
        self.assertEqual(resp.data["mensagem_fechamento"], "Chuva forte")

        resp = self.client.patch(url, {"aberto": True}, format="json")
        self.assertEqual(resp.data["status"], "aberto")
        self.assertEqual(resp.data["mensagem_fechamento"], "")

    def test_fechar_sem_mensagem_usa_mensagem_padrao(self):
        self.client.force_authenticate(self.admin)
        resp = self.client.patch(f"/api/parques/{self.parque.id}/status/", {"aberto": False}, format="json")
        self.assertEqual(resp.data["mensagem_fechamento"], "Parque temporariamente fechado.")

    def test_anonimo_nao_altera_status(self):
        resp = self.client.patch(f"/api/parques/{self.parque.id}/status/", {"aberto": False}, format="json")
        self.assertEqual(resp.status_code, 401)

    # ---- validações ----
    def test_aviso_com_trilha_de_outro_parque_e_rejeitado(self):
        outro = Parque.objects.create(nome="Outro")
        trilha = Trilha.objects.create(parque=outro, nome="T", duracao_estimada="1h")
        self.client.force_authenticate(self.admin)
        resp = self.client.post(
            "/api/avisos/",
            {"parque": self.parque.id, "trilha": trilha.id, "mensagem": "x"},
            format="json",
        )
        self.assertEqual(resp.status_code, 400)

    # ---- login ----
    def test_login_funcionario_retorna_token(self):
        resp = self.client.post("/api/auth/login/", {"email": "admin@x.com", "senha": "senha12345"}, format="json")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("token", resp.data)

    def test_login_senha_errada(self):
        resp = self.client.post("/api/auth/login/", {"email": "admin@x.com", "senha": "errada"}, format="json")
        self.assertEqual(resp.status_code, 401)

    def test_login_bloqueia_usuario_sem_is_staff(self):
        resp = self.client.post("/api/auth/login/", {"email": "comum@x.com", "senha": "senha12345"}, format="json")
        self.assertEqual(resp.status_code, 401)

    def test_contato(self):
        resp = self.client.get("/api/contato/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("telefone", resp.data)
