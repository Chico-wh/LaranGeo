# 🚍 Larangeo - Backend (Django)

[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

Larangeo é o backend de um sistema de monitoramento em tempo real de ônibus urbanos. O objetivo é fornecer dados de localização, status operacional e estimativas de tempo de chegada para passageiros via aplicativo mobile.

O frontend mobile foi desenvolvido com **React Native** e consome tanto a API REST quanto os **WebSockets** deste backend.

Este projeto foi idealizado a partir de um problema observado na vida real: a falta de informações sobre ônibus urbanos, que gera atrasos e dificulta o planejamento dos passageiros.

---

## 🧭 Tabela de Conteúdo

- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Execução](#-execução)
- [API e WebSockets](#-api-e-websockets)
- [Modelos de Dados](#-modelos-de-dados)
- [Como Contribuir](#-como-contribuir)
- [Licença](#-licença)
- [Autor](#-autor)

---

## ✨ Funcionalidades

O backend oferece:

- 📍 Rastreamento em tempo real de ônibus via WebSockets
- 🚦 Status operacional (ex: em operação, parado, manutenção, atrasado)
- 📊 Filtros por linha, destino e pontos de parada
- 🚏 Cadastro de pontos de parada e rotas
- ⏱️ Estimativa de tempo de chegada (ETA)
- 📱 Integração com frontend mobile (React Native)
- 🧩 Estrutura modular para fácil expansão

---

## 🛠️ Tecnologias

**Backend**
- Python 3.9+
- Django
- Django REST Framework
- Django Channels
- PostgreSQL / SQLite
- Redis (opcional)

**Frontend Mobile**
- React Native

---

## 🏗️ Arquitetura do Projeto


backend/
├── core/
├── apps/
│ ├── authentication/
│ ├── transporte/
│ └── stops/
├── websocket/
├── services/
├── api/
└── manage.py


---

## ⚙️ Instalação

1. Clone o repositório:

```bash
git clone https://github.com/Chico-wh/LaranGeo/edit/main/README.md

Crie e ative o ambiente virtual:

python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

Instale dependências:

pip install -r requirements.txt

Configure variáveis de ambiente:

Crie um arquivo .env com:

SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
▶️ Execução

Aplique as migrações:

python manage.py migrate

Inicie o servidor Django:

python manage.py runserver

O backend estará disponível em:

http://localhost:8000
🔌 API & WebSockets
REST

A API expõe endpoints para listar linhas, pontos e status.

Exemplo de filtro:

GET /api/buses/?line=402&destination=Centro
WebSockets

Use o endpoint WebSocket para receber atualizações em tempo real:

ws://localhost:8000/ws/tracking/

Exemplo de mensagem enviada pelo motorista ao servidor:

{
  "bus_id": "123",
  "line": "402",
  "destination": "Centro",
  "status": "operational",
  "lat": -22.9028,
  "lng": -43.2075,
  "timestamp": "2026-02-24T14:30:00"
}

Exemplo de mensagem retornada ao app:

{
  "bus_id": "123",
  "line": "402",
  "status": "on_time",
  "eta": 5,
  "location": {
    "lat": -22.9028,
    "lng": -43.2075
  }
}
🧩 Modelos de Dados (Resumido)

Bus — armazena identificação, linha e status

Stop — pontos de parada com coordenadas e ordem na rota

Route — conjunto de paradas que compõem uma linha

🤝 Como Contribuir

Contribuições são bem-vindas!

Faça um fork

Crie uma branch (feature/nova-feature)

Commit suas mudanças

Abra um Pull Request

📄 Licença

Este projeto está licenciado sob a MIT License.

👤 Autor

Felipe Santos — Backend & Mobile Developer

Projeto Larangeo — democratizando informações de transporte público.
