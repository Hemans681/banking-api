# Banking API

A production-ready REST API for core banking operations built with **Django** and **Django REST Framework**. Designed with clean architecture, containerised with Docker, and enforced with automated CI/CD and code quality checks.

---

## Features

- Account management — create, view, and manage bank accounts
- Deposit and withdrawal operations with validation
- Transaction history per account
- Token-based authentication (JWT)
- Dockerised for consistent local and production environments
- CI/CD pipeline via GitHub Actions
- Code quality enforced with Pylint, ruff, Flake8, and Pytest

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django, Django REST Framework |
| Database | SQLite (dev) |
| Auth | Token / JWT |
| Containerisation | Docker |
| CI/CD | GitHub Actions |
| Testing | Pytest |
| Code Quality | Pylint, Flake8, Black |

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker (optional but recommended)

### Run with Docker

```bash
git clone https://github.com/Hemans681/banking-api.git
cd banking-api
docker build -t banking-api .
docker run -p 8000:8000 banking-api
```

### Run locally

```bash
git clone https://github.com/Hemans681/banking-api.git
cd banking-api
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

API will be available at `http://localhost:8000`

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/` | Create a new account |
| GET | `/api/accounts/<id>/` | Get account details |
| POST | `/api/accounts/<id>/deposit/` | Deposit funds |
| POST | `/api/accounts/<id>/withdraw/` | Withdraw funds |
| GET | `/api/accounts/<id>/transactions/` | View transaction history |

> Full API docs available at `/api/schema/` when running locally.

---

## Running Tests

```bash
pytest
```

---

## CI/CD

GitHub Actions workflow runs on every push to `master`:
- Installs dependencies
- Runs Pylint and Flake8 checks
- Executes Pytest suite

---

## Project Structure

```
banking-api/
├── banking_accounts/     # Core app — models, views, serializers
├── banking_project/      # Django project settings
├── .github/workflows/    # CI/CD pipeline
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── pyproject.toml
└── manage.py
```

---

## Author

**Himanshu Srivastava** — [LinkedIn](https://www.linkedin.com/in/himanshu-srivastava-6a9089145/) · [GitHub](https://github.com/Hemans681)
