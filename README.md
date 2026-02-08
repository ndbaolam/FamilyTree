# Family Tree Web App

A modern, containerized web application to store, visualize, and manage a family tree. It features a graph-based backend, an interactive Vue.js frontend, and a secure admin dashboard.

![Tech Stack](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vue.js)
![Tech Stack](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/Neo4j-5-008CC1?style=flat&logo=neo4j)
![Tech Stack](https://img.shields.io/badge/MinIO-RELEASE.2025-C72C48?style=flat&logo=minio)
![Tech Stack](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)

## Features

- **Interactive Visualization**: Zoomable, pannable family tree graph (powered by Vue Flow).
- **Ordered Layout**: Displays generations in rows, automatically positioned.
- **Public Read-Only View**: Guests can view the tree but cannot edit it.
- **Admin Dashboard**: Secure area to manage people and relationships.
    - **Person Management**: Add/Edit profiles with details (Name, Gender, Dates, Biography).
    - **Avatar Upload**: Upload profile pictures for family members (stored in MinIO).
    - **Relationship Management**: Visually create connections or delete them via the dashboard.
- **Graph Database**: Uses Neo4j for efficient relationship storage and querying.
- **Secure Configuration**: Environment variables for sensitive credentials.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd family-tree
   ```

2. **Configure Environment**:
   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   Modify `.env` if you wish to change default credentials.

3. **Start the application**:
   ```bash
   docker compose up -d --build
   ```
   This initializes:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **Neo4j Database**: http://localhost:7474 (User/Pass from `.env`)
   - **MinIO Console**: http://localhost:9001 (User/Pass from `.env`)

4. **Access the App**:
   - Open [http://localhost](http://localhost) or [http://localhost:5173](http://localhost:5173).
   - **To Edit**: Navigate to `/login` (or click "Admin Login" if available).
     - **Default Password**: `admin123` (configurable in `.env`)

## Deployment to Server

To deploy on a remote server (e.g., VPS with IP `1.2.3.4`):

1. **Clone & Configure**: Follow steps 1-2 above.
2. **Update `.env`**:
   - `VITE_API_URL`: Set to `http://1.2.3.4:8000` (or your domain).
   - `PUBLIC_MINIO_URL`: Set to `http://1.2.3.4:9000`.
   - `ALLOWED_ORIGINS`: Set to `http://1.2.3.4,http://1.2.3.4:5173` (comma-separated).
3. **Build & Run**:
   ```bash
   docker compose up -d --build
   ```
   *Note: Frontend build bakes the API URL into the static files, so you MUST rebuild if you change `VITE_API_URL`.*

## Usage Guide

### Public User
- View the tree structure.
- Click on any node to see detailed information in the side panel.

### Administrator
1. **Login**: Go to the login page (`/login`) and enter the admin password.
2. **Dashboard**: Navigate to `/admin`.
3. **Manage People**:
   - **Add**: Use the "Add Person" button.
   - **Edit/Upload Avatar**: Click "Edit" on a person in the list. You can update their details and upload a profile picture.
   - **Delete**: Remove a person and their relationships.
4. **Connect People**:
   - On the main tree view (while logged in as admin), drag a line from the handle of one person to another to create a `PARENT_OF` relationship.

## Development

### Project Structure

```
.
├── be/                 # Backend (FastAPI)
│   ├── app/            # Application logic (models, database, storage)
│   ├── main.py         # API Endpoints
│   ├── debug_db.py     # Script to inspect DB content
│   └── Dockerfile
├── ui/                 # Frontend (Vue 3 + Pinia + Vue Flow)
│   ├── src/
│   │   ├── components/ # UI Components (Modals, Panels)
│   │   ├── stores/     # State Management (Pinia)
│   │   ├── views/      # Page Views (Tree, Admin, Login)
│   │   └── router/     # Navigation Routing
│   └── Dockerfile
├── docker-compose.yaml # Service Orchestration
├── .env                # Environment Configuration (GitIgnored)
└── .env.example        # Example Configuration
```

### Key Commands

- **Restart Backend**: `docker compose restart backend`
- **View Logs**: `docker compose logs -f backend`
- **Rebuild Services**: `docker compose up -d --build`

### Troubleshooting

- **500 Internal Server Error (Missing IDs)**:
  If legacy data is missing IDs, run the migration script:
  ```bash
  docker compose exec backend python migrate_ids.py
  ```

- **Database Connection**:
  Ensure Neo4j is ready. It accesses `neo4j_data` volume. If you need to reset the DB, `docker compose down -v` (CAUTION: deletes all data).

- **MinIO Access**:
  Ensure port 9000 (API) and 9001 (Console) are available. Check `.env` for credentials.
