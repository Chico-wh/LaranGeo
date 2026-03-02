

# 🚍 Larangeo - Backend (Django)

[![Status](https://img.shields.io/badge/status-in%20development-yellow)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

Larangeo is the backend of a real-time urban bus monitoring system.  
Its goal is to provide location data, operational status, and estimated arrival times to passengers through a mobile app.

The mobile frontend was developed with **React Native** and consumes both the **REST API** and **WebSockets** provided by this backend.

This project was inspired by a real-world problem: the lack of reliable public transport information, which causes delays and makes passenger planning difficult.

---

## 🧭 Table of Contents

- [Features](#-features)
- [Technologies](#-technologies)
- [Project Architecture](#-project-architecture)
- [Installation](#-installation)
- [Running the Project](#-running-the-project)
- [API and WebSockets](#-api-and-websockets)
- [Data Models](#-data-models)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## ✨ Features

The backend provides:

- 📍 Real-time bus tracking via WebSockets
- 🚦 Operational status (e.g., running, stopped, maintenance, delayed)
- 📊 Filters by line, destination, and stops
- 🚏 Registration of stops and routes
- ⏱️ Estimated Time of Arrival (ETA)
- 📱 Integration with React Native mobile app
- 🧩 Modular structure for easy expansion

---

## 🛠️ Technologies

### Backend
- Python 3.9+
- Django
- Django REST Framework
- Django Channels
- PostgreSQL / SQLite
- Redis (optional)

### Mobile Frontend
- React Native

---

## 🏗️ Project Architecture

```

backend/
├── core/
├── apps/
│   ├── authentication/
│   ├── transporte/
│   └── stops/
├── websocket/
├── services/
├── api/
└── manage.py

````

---

## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/Chico-wh/LaranGeo.git
cd LaranGeo
````

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

Create a `.env` file with:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

---

## ▶️ Running the Project

1. Apply migrations:

```bash
python manage.py migrate
```

2. Start the Django server:

```bash
python manage.py runserver
```

The backend will be available at:

```
http://localhost:8000
```

---

## 🔌 API and WebSockets

### REST API

The API provides endpoints to list bus lines, stops, and statuses.

Example filter:

```
GET /api/buses/?line=402&destination=Downtown
```

---

### WebSockets

Use the WebSocket endpoint to receive real-time updates:

```
ws://localhost:8000/ws/tracking/
```

#### Example message sent by the driver:

```json
{
  "bus_id": "123",
  "line": "402",
  "destination": "Downtown",
  "status": "operational",
  "lat": -22.9028,
  "lng": -43.2075,
  "timestamp": "2026-02-24T14:30:00"
}
```

#### Example message sent to the app:

```json
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
```

---

## 🧩 Data Models (Summary)

* **Bus** — stores identification, line, and status
* **Stop** — bus stops with coordinates and order in the route
* **Route** — set of stops that make up a bus line

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the project
2. Create a branch (`feature/new-feature`)
3. Commit your changes
4. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

Felipe Santos — Backend & Mobile Developer

Larangeo Project — democratizing public transport information.
