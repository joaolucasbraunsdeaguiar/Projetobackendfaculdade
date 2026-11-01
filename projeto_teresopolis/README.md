README Informativo

O repositório no GitHub deve incluir um arquivo README.md informativo que contenha as seguintes informações:

●     Dados dos integrantes da equipe: João Lucas Brauns de Aguiar (Matricula: 06012524)
●     Escolha da situação-problema: Circuito Terê Verde
●     Descrição sucinta do MVP: 

**MVP Back-End: Sistema de Gestão e Informações dos Parques de Teresópolis**

API REST em Python (Django REST Framework) que armazena e disponibiliza as informações dos três parques de Teresópolis: Parque Nacional da Serra dos Órgãos, Parque Estadual dos Três Picos e Parque Natural Municipal Montanhas de Teresópolis. O site é a interface de apresentação, e o back-end cuida dos dados, das regras e do acesso.

**Área pública (sem login):** consulta dos parques, horários, trilhas, eventos e avisos de manutenção, com identificação de parque aberto ou fechado. Quando fechado, a API devolve a mensagem exibida na faixa vermelha de "Parque Fechado".

**Área administrativa (funcionários):** login por e-mail e senha com autenticação por token. Os funcionários cadastram, editam e excluem parques, trilhas, eventos e avisos, atualizam horários e alteram o status de funcionamento. As operações de escrita só são aceitas de usuários com perfil de funcionário.

**Estrutura de dados:** cinco entidades (Parque, Trilha, Evento, Aviso e Usuário). Um parque tem várias trilhas, eventos e avisos, e um aviso pode estar ligado a uma trilha específica.

**Entregáveis:** endpoints REST documentados, um comando para popular o banco com dados de exemplo, testes automatizados dos principais fluxos (permissões, abrir e fechar parque, login e validações) e um README com instruções de execução.

**Tecnologias:** Python, Django, Django REST Framework, SQLite no desenvolvimento (com possibilidade de migrar para PostgreSQL) e CORS configurado para o front-end em HTML/CSS/JS.

●     Instruções para executar o MVP localmente: 

## Como rodar

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations   # gera as migrações dos 4 apps
python manage.py migrate
python manage.py seed             # 3 parques de exemplo + usuário ADM
python manage.py runserver
python manage.py test             # roda os testes
```

# Sistema de Gestão e Informações dos Parques de Teresópolis — MVP Back-End

API REST em **Python + Django REST Framework** para os três parques de Teresópolis
(Serra dos Órgãos, Três Picos e Montanhas de Teresópolis). O front-end (Home, Detalhes
do Parque, Contatos, Painel ADM) consome esta API.

API em `http://127.0.0.1:8000/api/` (o navegador mostra a interface navegável do DRF).
Usuário ADM criado pelo `seed`: `admin@teresopolis.rj.gov.br` / `admin12345` (troque em produção).
Painel Django extra: `http://127.0.0.1:8000/admin/` (usuário `admin`).

## Telas do protótipo × API

| Tela | Endpoint |
|---|---|
| Home: carrossel e cards dos parques | `GET /api/parques/` |
| Detalhes: info geral, trilhas, eventos, avisos, faixa vermelha "Parque Fechado" | `GET /api/parques/{id}/` |
| Eventos e Trilhas | `GET /api/eventos/?proximos=1` e `GET /api/trilhas/` |
| Contatos | `GET /api/contato/` |
| Contatos → Área Administrativa (login) | `POST /api/auth/login/` |
| Painel ADM: Eventos / Horários / Trilhas / Avisos | `POST/PUT/PATCH/DELETE` nos endpoints abaixo |
| Painel ADM: Sair | `POST /api/auth/logout/` |

No detalhe do parque, `status` é `"aberto"` ou `"fechado"`; quando fechado,
`mensagem_fechamento` traz o texto da faixa vermelha e `horario_exibicao` vem como
"Fechado temporariamente".

## Endpoints

Leitura (GET) é pública. Escrita exige `Authorization: Token <token>` de um funcionário (`is_staff`).

| Método | Endpoint | Função |
|---|---|---|
| GET | `/api/parques/` | Listar parques |
| GET | `/api/parques/1/` | Detalhe (com trilhas, próximos eventos e avisos ativos) |
| POST / PUT / PATCH / DELETE | `/api/parques/` e `/api/parques/1/` | CRUD de parques (ADM) |
| PATCH | `/api/parques/1/status/` | Abrir/fechar parque (ADM) |
| GET / POST ... | `/api/trilhas/` (`?parque=1&em_manutencao=true`) | Trilhas |
| GET / POST ... | `/api/eventos/` (`?parque=1&proximos=1`) | Eventos |
| GET / POST ... | `/api/avisos/` (`?parque=1`) | Avisos de manutenção/interdição (público vê só os ativos) |
| POST | `/api/auth/login/` | Login: `{"email": "...", "senha": "..."}` |
| POST | `/api/auth/logout/` | Invalida o token |
| GET | `/api/auth/me/` | Funcionário logado |
| GET | `/api/contato/` | Telefone, e-mail e endereço |

### Exemplos

```bash
# login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@teresopolis.rj.gov.br","senha":"admin12345"}'

# fechar o parque 1
curl -X PATCH http://127.0.0.1:8000/api/parques/1/status/ \
  -H "Authorization: Token SEU_TOKEN" -H "Content-Type: application/json" \
  -d '{"aberto": false, "mensagem_fechamento": "Fechado por causa da chuva."}'

# publicar evento (aba Eventos do painel)
curl -X POST http://127.0.0.1:8000/api/eventos/ \
  -H "Authorization: Token SEU_TOKEN" -H "Content-Type: application/json" \
  -d '{"parque":1,"titulo":"Trilha Noturna","data":"2026-11-30","descricao":"Saída às 18h."}'
```

## Estrutura

```
projeto_teresopolis/
├── config/      settings, urls, wsgi
├── parques/     modelo Parque, status aberto/fechado, contato, comando seed
├── trilhas/     modelo Trilha (dificuldade, duração, em manutenção)
├── eventos/     modelo Evento
├── avisos/      modelo Aviso (manutenção/interdição)
├── usuarios/    login por token e permissão IsAdminOrReadOnly
└── manage.py
```

## Banco de dados

| Tabela | Relações |
|---|---|
| Parque | 1 parque → N trilhas, N eventos, N avisos |
| Trilha | pertence a um parque |
| Evento | pertence a um parque |
| Aviso | pertence a um parque; pode apontar para uma trilha |
| Usuário | `auth.User` do Django; `is_staff=True` = funcionário ADM |

## Observações do MVP

- Horários e endereços de Três Picos e Montanhas de Teresópolis estão como "A confirmar" no `seed`: ajuste pelo ADM.
- Imagens são referenciadas por URL (`imagem_url`); upload de arquivos fica como evolução.
- Banco SQLite para desenvolvimento; para produção, trocar por PostgreSQL e definir `DJANGO_SECRET_KEY`, `DJANGO_DEBUG=0` e `ALLOWED_HOSTS`.
