# 🕵️‍♂️ OSINT Dashboard

A modern Open Source Intelligence (OSINT) dashboard built with **FastAPI** and **React**, orchestrated via Docker. It runs `theHarvester` and `Amass` in parallel, aggregates & deduplicates discovered data (emails, subdomains, IPs, etc.), and persists scan history for further analysis and export.

---

##  Quick Start

```bash
git clone https://github.com/mocharish/OSINT-Web-App.git
cd osint-dashboard
docker compose up --build
```

Then navigate to http://localhost:3000 to begin scanning.

---

## Project Overview
### Features

- Accepts a domain name (e.g., example.com) to initiate a scan

- Runs theHarvester and Amass in parallel using asyncio

- Deduplicates and merges discovered artifacts (emails, subdomains, IPs)

- Stores scan history in SQLite – persists on browser refresh

- View results in detail using responsive UI with modal dialogs

- Export any scan to Excel (XLSX)

- Built with testability and extensibility in mind

- Uses classic design patterns (Factory, Strategy)

- REST API built with FastAPI, and a responsive frontend in React

---

## Folder Structure

.
├── backend/
│   ├── main.py              # FastAPI app
│   ├── scanner/
│   │   ├── core.py          # Scanner logic and base classes
│   │   ├── factory.py       # Factory pattern to instantiate scanners
│   │   ├── parser.py        # Artifact parsing & deduplication
│   │   ├── storage.py       # SQLite history persistence
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   └── App.js           # React 
│   └── package.json
├── docker-compose.yml       # Multi-service Docker orchestrator
├── Dockerfile.backend       # FastAPI container
├── Dockerfile.frontend      # React container
├── README.md                
└── answers.md               # Deployment, testing, performance insights


## Dockerized Stack

### docker-compose.yml includes:

- Backend: FastAPI app with theHarvester and Amass

- Frontend: React UI served via Nginx

- Database: SQLite volume for persistent scan history


## Implementation Details

- theHarvester and Amass are pre-installed in the backend container

- Parallel execution is managed using asyncio.gather()

- Artifact deduplication leverages sets and value-keying (normalized data)

- SQLite stores full scan results and timestamps

- Export to Excel uses openpyxl for downloadable .xlsx reports


## Deployment
A public Docker image is published here:

```bash
docker pull mocharish/osint-dashboard-backend:latest
docker pull mocharish/osint-dashboard-frontend:latest
```


##  Tests

Backend tests are included in the `backend/tests/` directory.

They are automatically executed inside the Docker environment using the `backend-tests` service:

```bash
docker compose run backend-tests
```
