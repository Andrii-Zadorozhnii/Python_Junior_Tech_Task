# 🌍 Nationality Guesser API 🇺🇳

An API that predicts the most likely nationality based on a given name.

## ⚙️ Requirements

- 🐳 [Docker](https://www.docker.com/)
- 📦 [Docker Compose](https://docs.docker.com/compose/)

## 🚀 Installation

1. 📥 Clone the repository:
   ```bash
   git clone https://github.com/your-username/nationality-guesser.git
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

---

## 🧾 Example `.env` Configuration

```env
POSTGRES_DB=nationality_db
POSTGRES_USER=nationality_user
POSTGRES_PASSWORD=complexpassword123

SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://nationality_user:complexpassword123@db:5432/nationality_db
```

---

## 📬 Contact

If you have any questions or suggestions, feel free to open an issue or reach out!

📫 Happy coding!