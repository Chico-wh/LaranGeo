<div align="center">

# 🚍 LaranGeo — Backend

**Sistema de rastreamento urbano de ônibus em tempo real**

[![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.16-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org/)
[![WebSocket](https://img.shields.io/badge/WebSockets-Django_Channels_4.3-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://channels.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](./LICENSE)
[![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow?style=for-the-badge)]()

---

*LaranGeo é o backend de um sistema de monitoramento urbano de ônibus em tempo real, fornecendo dados de localização, status operacional e estimativas de chegada a um aplicativo mobile React Native via REST API e WebSockets.*

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Stack Tecnológica](#-stack-tecnológica)
- [Arquitetura do Projeto](#-arquitetura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação e Configuração](#-instalação-e-configuração)
- [Executando o Projeto](#-executando-o-projeto)
- [API REST — Endpoints](#-api-rest--endpoints)
- [WebSockets — Rastreamento em Tempo Real](#-websockets--rastreamento-em-tempo-real)
- [Modelos de Dados](#-modelos-de-dados)
- [Autenticação](#-autenticação)
- [Deploy (Produção)](#-deploy-produção)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)
- [Autor](#-autor)

---

## 🌐 Sobre o Projeto

O **LaranGeo** nasceu da necessidade real de democratizar o acesso à informação sobre transporte público urbano. A falta de dados confiáveis sobre localização e chegada dos ônibus causa atrasos, frustração e impacta diretamente a qualidade de vida dos passageiros.

Este backend serve como o núcleo do sistema, responsável por:

- Receber atualizações de localização dos motoristas em tempo real
- Processar e distribuir essas informações via WebSocket para os passageiros
- Calcular estimativas de tempo de chegada (ETA) para cada parada
- Gerenciar rotas, linhas, paradas e status operacional dos veículos

O frontend mobile foi desenvolvido em **React Native** e consome tanto a **REST API** quanto os **WebSockets** fornecidos por este backend.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 📍 **Rastreamento em Tempo Real** | Localização GPS dos ônibus transmitida via WebSocket |
| 🚦 **Status Operacional** | Controle de estados: `operational`, `stopped`, `maintenance`, `delayed` |
| ⏱️ **ETA (Tempo de Chegada)** | Estimativa de chegada calculada por parada e linha |
| 🚏 **Gestão de Paradas** | Cadastro e consulta de pontos com coordenadas geográficas |
| 🗺️ **Gestão de Rotas** | Conjunto ordenado de paradas que compõem uma linha de ônibus |
| 🔍 **Filtros Avançados** | Filtros por linha, destino e paradas |
| 🔐 **Autenticação JWT** | Segurança via tokens JWT com `djangorestframework-simplejwt` |
| 📱 **Integração Mobile** | API projetada para consumo pelo app React Native |
| 🧩 **Estrutura Modular** | Apps Django independentes para fácil expansão |

---

## 🛠️ Stack Tecnológica

### Backend

| Tecnologia | Versão | Finalidade |
|---|---|---|
| Python | 3.9+ | Linguagem base |
| Django | 5.2 | Framework web principal |
| Django REST Framework | 3.16 | Construção da API REST |
| Django Channels | 4.3 | Suporte a WebSockets e ASGI |
| Daphne | 4.0 | Servidor ASGI para produção |
| Uvicorn | 0.38 | Servidor ASGI para desenvolvimento |
| PostgreSQL | — | Banco de dados em produção |
| SQLite | — | Banco de dados em desenvolvimento |
| Redis | 7.0 | Canal layer para Django Channels |
| SimpleJWT | 5.5 | Autenticação via tokens JWT |
| python-dotenv | 1.2 | Gerenciamento de variáveis de ambiente |
| WhiteNoise | 6.11 | Servir arquivos estáticos em produção |
| django-cors-headers | — | Controle de CORS para o app mobile |

### Mobile (Frontend Integrado)

| Tecnologia | Finalidade |
|---|---|
| React Native | Interface do passageiro |

---

## 🏗️ Arquitetura do Projeto

```
LaranGeo/
│
├── core/                        # Configurações centrais do Django
│   ├── settings.py              # Configurações gerais (DB, apps, channels)
│   ├── urls.py                  # Roteamento principal
│   ├── asgi.py                  # Ponto de entrada ASGI (HTTP + WebSocket)
│   └── wsgi.py                  # Ponto de entrada WSGI (fallback)
│
├── authentication/              # App de autenticação de usuários
│   ├── models.py                # Modelo de usuário customizado (se houver)
│   ├── views.py                 # Endpoints de login, registro e refresh
│   ├── serializers.py           # Serialização de dados de autenticação
│   └── urls.py                  # Rotas de autenticação
│
├── transporte/                  # App principal — lógica de negócio
│   ├── models.py                # Modelos: Bus, Stop, Route
│   ├── views.py                 # ViewSets da API REST
│   ├── serializers.py           # Serialização dos modelos
│   ├── consumers.py             # WebSocket consumers (rastreamento)
│   ├── routing.py               # Rotas WebSocket
│   └── urls.py                  # Rotas REST
│
├── fixtures/                    # Dados iniciais para popular o banco
│   └── *.json                   # Fixtures de linhas, paradas e rotas
│
├── manage.py                    # CLI do Django
├── procfile                     # Comando de inicialização para deploy (Heroku/Railway)
├── requirements.txt             # Dependências Python
└── db.sqlite3                   # Banco SQLite (desenvolvimento)
```

### Fluxo de Dados

```
[Motorista / App do Motorista]
        │
        │  WebSocket (envia localização GPS)
        ▼
[Django Channels Consumer]
        │
        │  Processa e distribui via Channel Layer (Redis)
        ▼
[Passageiros / App React Native]
        │
        │  WebSocket (recebe posição + ETA em tempo real)
        ▼
[Interface do Passageiro — Mapa ao vivo]
```

---

## ✅ Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- [Python 3.9+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/)
- [Redis](https://redis.io/download/) *(para suporte a WebSockets com múltiplos workers)*
- [PostgreSQL](https://www.postgresql.org/) *(opcional — SQLite para dev local)*
- [Git](https://git-scm.com/)

---

## ⚙️ Instalação e Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/Chico-wh/LaranGeo.git
cd LaranGeo
```

### 2. Crie e ative o ambiente virtual

```bash
# Criar
python -m venv venv

# Ativar (Linux / macOS)
source venv/bin/activate

# Ativar (Windows)
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3

# Para produção com PostgreSQL:
# DATABASE_URL=postgres://user:password@localhost:5432/larangeo

# Redis (para Django Channels com múltiplos workers)
REDIS_URL=redis://localhost:6379/0

# CORS (origens permitidas para o app mobile)
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8081
```

### 5. Aplique as migrações

```bash
python manage.py migrate
```

### 6. (Opcional) Carregue os dados iniciais

```bash
python manage.py loaddata fixtures/*.json
```

### 7. Crie um superusuário

```bash
python manage.py createsuperuser
```

---

## ▶️ Executando o Projeto

### Desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em: **http://localhost:8000**

O painel de administração estará em: **http://localhost:8000/admin/**

### Desenvolvimento com suporte completo a WebSockets

Para testar WebSockets localmente com Uvicorn:

```bash
uvicorn core.asgi:application --reload --host 0.0.0.0 --port 8000
```

---

## 🔌 API REST — Endpoints

### Autenticação

| Método | Endpoint | Descrição |
|---|---|---|
| `POST` | `/api/token/` | Obter par de tokens (access + refresh) |
| `POST` | `/api/token/refresh/` | Renovar o access token |

**Exemplo — Login:**
```bash
POST /api/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### Transporte

| Método | Endpoint | Descrição |
|---|---|---|
| `GET` | `/api/buses/` | Listar todos os ônibus |
| `GET` | `/api/buses/?line=402` | Filtrar por linha |
| `GET` | `/api/buses/?line=402&destination=Centro` | Filtrar por linha e destino |
| `GET` | `/api/buses/{id}/` | Detalhes de um ônibus |
| `GET` | `/api/stops/` | Listar todas as paradas |
| `GET` | `/api/stops/{id}/` | Detalhes de uma parada |
| `GET` | `/api/routes/` | Listar todas as rotas |
| `GET` | `/api/routes/{id}/` | Detalhes de uma rota |

> 💡 Todos os endpoints de listagem suportam paginação e filtros via query params.

---

## 📡 WebSockets — Rastreamento em Tempo Real

### Endpoint WebSocket

```
ws://localhost:8000/ws/tracking/
```

Em produção:
```
wss://seu-dominio.com/ws/tracking/
```

---

### Mensagem enviada pelo motorista (entrada)

O app do motorista envia atualizações de posição:

```json
{
  "bus_id": "123",
  "line": "402",
  "destination": "Centro",
  "status": "operational",
  "lat": -22.9028,
  "lng": -43.2075,
  "timestamp": "2026-05-06T14:30:00"
}
```

**Status possíveis:**

| Valor | Descrição |
|---|---|
| `operational` | Em operação normal |
| `stopped` | Parado temporariamente |
| `maintenance` | Em manutenção |
| `delayed` | Com atraso |

---

### Mensagem enviada para o passageiro (saída)

O backend processa e distribui para todos os clientes conectados:

```json
{
  "bus_id": "123",
  "line": "402",
  "destination": "Centro",
  "status": "on_time",
  "eta": 5,
  "location": {
    "lat": -22.9028,
    "lng": -43.2075
  },
  "timestamp": "2026-05-06T14:30:00"
}
```

> `eta` é o tempo estimado de chegada à próxima parada, em minutos.

---

## 🧩 Modelos de Dados

### Bus (Ônibus)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | AutoField | Identificador único |
| `line` | CharField | Número/código da linha |
| `destination` | CharField | Destino final |
| `status` | CharField | Status operacional atual |
| `lat` | FloatField | Latitude atual |
| `lng` | FloatField | Longitude atual |
| `updated_at` | DateTimeField | Última atualização de posição |

### Stop (Parada)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | AutoField | Identificador único |
| `name` | CharField | Nome da parada |
| `lat` | FloatField | Latitude da parada |
| `lng` | FloatField | Longitude da parada |
| `order` | IntegerField | Ordem dentro da rota |

### Route (Rota)

| Campo | Tipo | Descrição |
|---|---|---|
| `id` | AutoField | Identificador único |
| `name` | CharField | Nome da linha/rota |
| `stops` | ManyToManyField | Paradas que compõem a rota |

---

## 🔐 Autenticação

O sistema utiliza **JWT (JSON Web Tokens)** via `djangorestframework-simplejwt`.

Para acessar endpoints protegidos, inclua o token no header da requisição:

```http
Authorization: Bearer <seu_access_token>
```

Os tokens têm validade configurável. Use o endpoint `/api/token/refresh/` para renovar o access token sem precisar fazer login novamente.

---

## 🚀 Deploy (Produção)

O projeto está preparado para deploy em plataformas como **Heroku** ou **Railway**, utilizando **Daphne** como servidor ASGI.

### Procfile

```
web: daphne -b 0.0.0.0 -p $PORT core.asgi:application
```

### Passos para deploy

1. Configure as variáveis de ambiente na plataforma de deploy (ver seção abaixo)
2. Configure um banco de dados PostgreSQL externo
3. Configure uma instância Redis (para o Channel Layer)
4. Execute as migrações no ambiente de produção:
   ```bash
   python manage.py migrate
   ```
5. Colete os arquivos estáticos:
   ```bash
   python manage.py collectstatic --noinput
   ```

O WhiteNoise já está configurado para servir arquivos estáticos sem necessidade de um servidor web separado.

---

## 🔧 Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|---|---|---|
| `SECRET_KEY` | ✅ | Chave secreta do Django |
| `DEBUG` | ✅ | `True` para dev, `False` para produção |
| `DATABASE_URL` | ✅ | URL de conexão com o banco de dados |
| `REDIS_URL` | ⚠️ | URL do Redis (necessário para WebSockets em produção) |
| `CORS_ALLOWED_ORIGINS` | ⚠️ | Origens permitidas pelo CORS |
| `ALLOWED_HOSTS` | ✅ em prod | Hosts permitidos pelo Django |

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um **fork** do projeto
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b feature/minha-feature
   ```
3. Faça o commit das suas alterações:
   ```bash
   git commit -m "feat: adiciona minha feature"
   ```
4. Envie para o repositório remoto:
   ```bash
   git push origin feature/minha-feature
   ```
5. Abra um **Pull Request**

> Siga a convenção de commits [Conventional Commits](https://www.conventionalcommits.org/) sempre que possível.

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License**. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

## 👤 Autor

**Felipe Santos** — Backend & Mobile Developer

> LaranGeo: democratizando o acesso à informação sobre transporte público urbano.

---

<div align="center">

Feito com ❤️ para melhorar o transporte público

</div>
