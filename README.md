# 🚍 Larangeo - Backend (Django)

Larangeo é o backend de um sistema de monitoramento em tempo real de ônibus urbanos, desenvolvido para fornecer informações precisas de localização, status operacional e estimativas de tempo aos passageiros por meio de um aplicativo mobile.

O projeto surgiu a partir da observação direta dos problemas enfrentados no transporte público municipal, onde a ausência de dados confiáveis impacta diretamente o planejamento diário da população.

---

## 📌 Visão Geral

O sistema permite que motoristas compartilhem sua localização e status em tempo real, enquanto passageiros acompanham a movimentação dos veículos diretamente no aplicativo, com filtros por linha, destino e pontos de parada.

A comunicação em tempo real é realizada por meio de WebSockets, garantindo baixa latência.

O frontend mobile foi desenvolvido em React Native.

---

## ✨ Funcionalidades

- 📍 Rastreamento em tempo real dos ônibus
- 🔄 Comunicação bidirecional via WebSockets
- 🚦 Compartilhamento de status operacional:
  - Em operação
  - Parado
  - Em manutenção
  - Atrasado
  - Fora de serviço
- 📱 Integração com aplicativo mobile
- 🔍 Filtros por linha, destino e paradas
- 🗺️ Visualização em mapa
- ⏱️ Cálculo estimado de tempo de chegada (ETA)
- 🚏 Cadastro e gerenciamento de pontos de parada
- 📊 Monitoramento da frota
- 🧩 Arquitetura modular

---

## 🛠️ Tecnologias Utilizadas

### Backend
- Python 3.9+
- Django
- Django Channels
- Django REST Framework
- PostgreSQL / SQLite
- Redis (opcional)

### Frontend
- React Native

---

## 🏗️ Arquitetura


backend/
├── core/
├── apps/
│ ├── tracking/
│ ├── routes/
│ ├── stops/
│ ├── fleet/
│ └── users/
├── websocket/
├── services/
├── api/
└── manage.py


---

## ⚙️ Pré-requisitos

- Python 3.9+
- pip
- Virtualenv

---

## 🚀 Instalação

```bash
git clone https://github.com/seu-usuario/larangeo-backend.git
cd larangeo-backend
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt
▶️ Execução
python manage.py migrate
python manage.py runserver
🔌 WebSocket
ws://localhost:8000/ws/tracking/
🔄 Exemplo de Atualização de Status
{
  "bus_id": "123",
  "line": "402",
  "destination": "Centro",
  "status": "maintenance",
  "lat": -22.9028,
  "lng": -43.2075,
  "timestamp": "2026-02-24T14:30:00"
}
🚏 Pontos de Parada

O sistema mantém um cadastro estruturado de pontos de parada, contendo:

Nome

Coordenadas geográficas

Linhas atendidas

Ordem na rota

Horários estimados

Esses dados são utilizados para cálculo de tempo e planejamento de rotas.

📊 Estimativa de Tempo (ETA)

O cálculo de ETA é baseado em:

Velocidade média do veículo

Histórico de tráfego

Distância até o ponto

Status atual

Eventos externos (congestionamentos)

Este módulo está em constante evolução.

📱 Aplicativo Mobile

Funcionalidades:

Mapa em tempo real

Status dos ônibus

Lista de paradas

Previsão de chegada

Alertas operacionais

📈 Roadmap

🤖 Machine Learning para previsão

🧠 Detecção automática de falhas

🔔 Notificações push

📊 Dashboard web

🌐 API pública

📄 Licença

MIT

👤 Autor

Felipe Santos
Backend & Mobile Developer

💬 Motivação

O Larangeo nasceu da necessidade de democratizar o acesso à informação no transporte público, reduzindo atrasos, frustração e ineficiência operacional.
