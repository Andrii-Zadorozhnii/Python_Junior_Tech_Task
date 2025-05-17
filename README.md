
# 🌍 Nationality Guesser API 🇺🇳

An API that predicts the most likely nationality based on a given name and provides country information.

## 📌 Project Preview

This service provides two main functionalities:
1. Predicts likely countries of origin for a given name using Nationalize.io API
2. Shows popular names associated with specific countries
3. Caches results for efficient retrieval and reduces external API calls

The system automatically fetches and stores country details from REST Countries API when new nationalities are encountered.

## 🛠 Tech Stack

### Backend
- **Python 3.11**
- **Django 4.2** (with Django REST Framework)
- **PostgreSQL** (Relational database)

### Infrastructure
- **Docker** (Containerization)
- **Docker Compose** (Orchestration)
- **Nginx** (Reverse proxy)

### Development Tools
- **Ruff** (Linting and formatting)
- **Pytest** (Testing framework)
- **Swagger/ReDoc** (API documentation)
- **JWT Authentication** (Secure API access)

## ⚙️ Requirements

- 🐳 [Docker](https://www.docker.com/)
- 📦 [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Installation

1. 📥 Clone the repository:
   ```bash
   git clone https://github.com/Andrii-Zadorozhnii/Python_Junior_Tech_Task.git
   cd nationality-guesser
   ```

2. 🛠️ Create the `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```

3. ▶️ Start the project using Docker Compose:
   ```bash
   docker-compose up -d
   ```

Welcome to web page for short preview  `http://localhost:8000`. Access login: admin / password: admin

---

## 🧾 Example `.env` Configuration

```env
# Database
POSTGRES_DB=nationality_db
POSTGRES_USER=nationality_user
POSTGRES_PASSWORD=complexpassword123

# Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://nationality_user:complexpassword123@db:5432/nationality_db

# Cache
REDIS_URL=redis://redis:6379/0

# External APIs
NATIONALIZE_API=https://api.nationalize.io/
RESTCOUNTRIES_API=https://restcountries.com/v3.1/
```

---

## 📬 Contact

If you have any questions or suggestions, feel free to open an issue or reach out!

📫 Happy coding!

---

### Key Features Not Shown in Sample
- **Automatic data refresh**: Stale data (older than 1 day) is automatically refreshed
- **Rate limiting**: Protection against excessive API calls
- **Comprehensive tests**: 90%+ test coverage
- **Efficient caching**: Redis-based caching layer for improved performance
