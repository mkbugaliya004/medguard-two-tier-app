# MedGuard – Antiarrhythmic Medication Safety and Monitoring - three-tier

## Project Overview

MedGuard is an educational medication safety and monitoring prototype designed to assess selected clinical parameters associated with three antiarrhythmic medicines:

- Sotalol
- Flecainide
- Amiodarone

The application uses synthetic patient profiles to demonstrate how medication-related checks, monitoring information and assessment results can be organised and presented through a web application.

**Project title:** Development and Validation of a Cloud-Based Antiarrhythmic Medication Safety and Monitoring Application Using Synthetic Clinical Profiles.

## Project Objectives

- Develop a web-based medication safety assessment application.
- Implement rule-based checks for selected antiarrhythmic medicines.
- Capture and manage synthetic patient profiles.
- Store patient information and assessment history in a relational database.
- Provide an interface for viewing assessment results and previous assessments.
- Use containerisation and automated testing to support deployment and software quality.

## Application Features

### 1. Medication Safety Assessment

The backend provides separate rule modules for:

- Sotalol
- Flecainide
- Amiodarone

The assessment service evaluates submitted patient information and returns a structured assessment response containing the assessment status, alerts and relevant information.

### 2. Patient Management

The application supports:

- Creating patient profiles.
- Retrieving individual patient records.
- Listing saved patient profiles.
- Updating patient information through the assessment workflow.

All patient records used in this prototype must be synthetic.

### 3. Assessment History

Assessment results are stored in PostgreSQL.

Users can retrieve previous assessments associated with a patient and review the recorded results.

### 4. Web Interface

The frontend provides:

- Medication assessment forms.
- Input validation.
- Assessment result presentation.
- Patient directory.
- Patient assessment history.

### 5. Database and Migrations

PostgreSQL is used for persistent data storage.

SQLAlchemy provides database ORM functionality, while Alembic manages database schema migrations.

## System Architecture

MedGuard uses a containerised web application architecture.

```text
             User / Browser
                   |
                   v
          Frontend – Nginx
          HTML, CSS, JavaScript
                   |
                   | REST API requests
                   v
             FastAPI Backend
                   |
          ---------------------
          |                   |
          v                   v
    Patient API         Assessment API
          |                   |
          |             Assessment Rules
          |          Sotalol / Flecainide /
          |               Amiodarone
          |                   |
          -----------+---------
                     |
                     v
              SQLAlchemy ORM
                     |
                     v
                PostgreSQL
```

### Main Components

| Component | Technology | Responsibility |
|---|---|---|
| Frontend | HTML, CSS, JavaScript | User interface and API requests |
| Web server | Nginx | Serves frontend and proxies API traffic |
| Backend | Python, FastAPI | API endpoints and assessment processing |
| ORM | SQLAlchemy | Database operations |
| Database | PostgreSQL 16 | Persistent patient and assessment records |
| Migrations | Alembic | Database schema management |
| Containers | Docker | Application packaging |
| Orchestration | Docker Compose | Running application services |
| CI | GitHub Actions | Automated backend tests and migration checks |

## Technology Stack

- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL 16
- Alembic
- HTML5
- CSS3
- JavaScript
- Nginx
- Docker
- Docker Compose
- Pytest
- GitHub Actions

## Repository Structure

```text
medguard-two-tier-app/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       └── endpoints/
│   │   │           ├── assessments.py
│   │   │           └── patients.py
│   │   │
│   │   ├── core/
│   │   ├── db/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── rules/
│   │   │   ├── amiodarone.py
│   │   │   ├── flecainide.py
│   │   │   └── sotalol.py
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tests/
│   │
│   ├── migrations/
│   ├── Dockerfile
│   ├── alembic.ini
│   └── requirements.txt
│
├── frontend/
│   ├── css/
│   ├── js/
│   │   ├── api.js
│   │   ├── app.js
│   │   ├── patients.js
│   │   └── validation.js
│   ├── Dockerfile
│   ├── index.html
│   └── nginx.conf
│
├── database/
│   └── init/
│
├── docs/
│
├── .dockerignore
├── .env.example
└── compose.yaml
```

## API Endpoints

The backend exposes versioned API endpoints under `/api/v1`.

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/v1/patients/` | Create a patient profile |
| GET | `/api/v1/patients/` | Retrieve patient directory |
| GET | `/api/v1/patients/{patient_id}` | Retrieve an individual patient |
| POST | `/api/v1/assessments/` | Submit a medication assessment |
| GET | `/api/v1/assessments/patient/{patient_id}` | Retrieve patient assessment history |
| GET | `/health` | Check backend health |

The FastAPI application also provides interactive API documentation at `/docs` when accessed directly through the backend.

## Prerequisites

Before running the application, ensure you have:

- Docker installed.
- Docker Compose installed.
- Git installed.
- A compatible Linux, Windows or macOS environment.

The current Nginx configuration is set up for HTTPS using the domain `medguard365.com`.

For the configured Compose deployment, the corresponding TLS certificate files must be available at:

```text
certbot/conf/live/medguard365.com/fullchain.pem
certbot/conf/live/medguard365.com/privkey.pem
```

The domain DNS must point to the deployment server. For local development without these certificates, the Nginx configuration must first be adapted for local HTTP access.

## Configuration

Clone the repository and switch to the development branch:

```bash
git clone https://github.com/mkbugaliya004/medguard-two-tier-app.git

cd medguard-two-tier-app

git checkout medguard-upgrade
```

Create a local environment file:

```bash
cp .env.example .env
```

Edit `.env` and replace the placeholder PostgreSQL password with a strong local password.

Keep `.env` private. Do not commit real credentials or secrets to GitHub.

## Running with Docker Compose

Once the environment variables and required HTTPS certificates are configured, build and start the services:

```bash
docker compose up --build -d
```

Check running containers:

```bash
docker compose ps
```

View application logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

The PostgreSQL database uses a named Docker volume so that its data can persist when containers are stopped or recreated.

To remove the containers and database volume permanently, use:

```bash
docker compose down -v
```

**Warning:** Removing the volume deletes the stored database data.

## Testing and Continuous Integration

The project uses Pytest for backend testing.

Run the tests locally:

```bash
cd backend

pip install -r requirements.txt

python -m pytest -v app/tests
```

Database migration validation:

```bash
DATABASE_URL=sqlite:///./migration_check.db alembic upgrade head
```

GitHub Actions runs automated checks when changes are pushed to or submitted through pull requests targeting the configured branches.

The current workflow validates database migrations and executes the backend test suite.

## Security and Data Considerations

- Use synthetic patient profiles only.
- Never upload real patient or identifiable clinical information.
- Keep database credentials and other secrets outside source control.
- Use HTTPS for the configured domain deployment.
- Restrict access to the application and its database in any hosted environment.
- Review and validate all medication rules before relying on their output.

## Important Clinical Disclaimer

MedGuard is an academic and educational software prototype. It is not a medical device, clinical decision-support system approved for patient care, or a substitute for professional medical judgement.

The medication rules and thresholds are draft implementations and require review against authoritative clinical guidance and supervisor approval. Assessment outputs must not be used to make real prescribing, diagnosis or treatment decisions.

The application currently uses synthetic clinical profiles only.

## Project Status

The project is under active development.

Current implementation includes:

- FastAPI backend.
- Patient management API.
- Medication assessment modules for three medicines.
- PostgreSQL persistence.
- Assessment history.
- Browser-based frontend.
- Docker Compose configuration.
- Database migrations.
- Automated backend testing through GitHub Actions.

Further development and validation are required before the application can be considered suitable for any real-world clinical environment.

## Repository

GitHub: https://github.com/mkbugaliya004/medguard-two-tier-app

Development branch: `medguard-upgrade`
