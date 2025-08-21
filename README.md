# Task Manager API
A robust and scalable Task Management API built with FastAPI, featuring full CRUD operations, PostgreSQL integration, and comprehensive testing.
## Features
- **Full CRUD Operations**: Create, Read, Update, Delete, and List tasks
    
- **PostgreSQL Database**: Reliable data storage with SQLAlchemy ORM
    
- **Alembic Migrations**: Database schema versioning and management
    
- **Pytest Testing**: Comprehensive test suite with high coverage
    
- **Poetry Dependency Management**: Clean and reproducible dependency management
    
- **Docker Containerization**: Easy development and deployment with Docker
    
- **Environment Configuration**: Flexible configuration through environment variables
## Tech Stack

- **Framework**: FastAPI
    
- **Database**: PostgreSQL
    
- **ORM**: SQLAlchemy
    
- **Migrations**: Alembic
    
- **Testing**: Pytest
    
- **Dependency Management**: Poetry
    
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose
    
- Python 3.12+ (for local development)
    
- Poetry (for local development)

## Quick Start (Docker - Recommended)

1. **Clone and setup environment**:

```bash
cp .env.example .env
# Edit .env if needed (defaults work for Docker)
```
2. **Start services**:
```bash
docker-compose up -d
```

3. **Migrations applied automatically in entrypoint.sh**
4. - **Access the application**:
    
    - API: [http://localhost:8000](http://localhost:8000/api)
        
    - API Documentation: [http://localhost:8000/docs](http://localhost:8000/api/docs)
        
    - Alternative Documentation: [http://localhost:8000/redoc](http://localhost:8000/api/redoc)

## API Endpoints

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/tasks`           | Get all tasks       |
| POST   | `/tasks`           | Create a new task   |
| GET    | `/tasks/{task_id}` | Get a specific task |
| PATCH  | `/tasks/{task_id}` | Update a task       |
| DELETE | `/tasks/{task_id}` | Delete a task       |
