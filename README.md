# Family Tree Web App

A modern, containerized web application to store, visualize, and manage a family tree. It features a graph-based backend, an interactive Vue.js frontend, and a secure admin dashboard.

![Tech Stack](https://img.shields.io/badge/Vue.js-3-4FC08D?style=flat&logo=vue.js)
![Tech Stack](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![Tech Stack](https://img.shields.io/badge/Neo4j-5-008CC1?style=flat&logo=neo4j)
![Tech Stack](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)

## Features

- **Interactive Visualization**: Zoomable, pannable family tree graph (powered by Vue Flow).
- **Ordered Layout**: Displays generations in rows, with siblings sorted by birth order (or custom order).
- **Public Read-Only View**: Guests can view the tree but cannot edit it.
- **Admin Dashboard**: Secure area to manage people and relationships.
    - **Person Management**: Add/Edit profiles with details (Name, Gender, Dates, Biography).
    - **Relationship Management**: visually create connections or delete them via the dashboard.
- **Graph Database**: Uses Neo4j for efficient relationship storage and querying.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd family-tree
   ```

2. **Start the application**:
   ```bash
   docker compose up -d --build
   ```
   This initializes:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **Neo4j Database**: http://localhost:7474 (User: `neo4j`, Password: `password`)

3. **Access the App**:
   - Open [http://localhost:5173](http://localhost:5173).
   - **To Edit**: Navigate to `/login`.
     - **Default Password**: `admin123`

## Usage Guide

### Public User
- View the tree structure.
- Click on any node to see detailed information in the side panel.

### Administrator
1. **Login**: Go to the login page and enter the admin password.
2. **Add Person**: Use the "Add Person" button in the top-left corner or the Admin Dashboard.
3. **Connect People**:
   - Drag a line from the handle (dot) of one person to another.
   - Default relationship is `PARENT_OF`.
4. **Delete Relationships**:
   - Go to `/admin` (Dashboard).
   - Switch to the "Relationships" tab.
   - Click "Delete" next to the relationship you want to remove.

## Development

### Project Structure

```
.
├── be/                 # Backend (FastAPI)
│   ├── app/            # Application logic (models, database)
│   ├── main.py         # API Endpoints
│   ├── debug_db.py     # Script to inspect DB content
│   ├── migrate_ids.py  # Script to fix missing UUIDs
│   └── Dockerfile
├── ui/                 # Frontend (Vue 3 + Pinia + Vue Flow)
│   ├── src/
│   │   ├── components/ # UI Components (Modals, Panels)
│   │   ├── stores/     # State Management (Pinia)
│   │   ├── views/      # Page Views (Tree, Admin, Login)
│   │   └── router/     # Navigation Routing
│   └── Dockerfile
└── docker-compose.yaml # Service Orchestration
```

### Key Commands

- **Restart Backend**: `docker compose restart backend`
- **View Logs**: `docker compose logs -f backend`
- **Rebuild Frontend**: `docker compose build frontend && docker compose up -d frontend`

### Troubleshooting

- **500 Internal Server Error (Missing IDs)**:
  If the API fails to load the tree, it might be due to manual data insertion missing the `id` property. Run the migration script:
  ```bash
  docker compose exec backend python migrate_ids.py
  ```

- **Database Connection**:
  Ensure Neo4j is ready. It accesses `neo4j_data` volume. If you need to reset the DB, `docker compose down -v` (CAUTION: deletes all data).
