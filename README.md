# Mental Journal Backend

A Flask-based backend for the Mental Journal application.

## Tech Stack

-   **Language**: Python 3.11
-   **Framework**: Flask 3.0.0
-   **Database**: SQLite (via SQLAlchemy ORM)
-   **Authentication**: JWT (JSON Web Tokens)
-   **Deployment**: Docker & Docker Compose

## Setup Instructions

### Prerequisites

-   Docker and Docker Compose installed.
-   Git installed.

### Environment Configuration

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open `.env` and fill in your values (e.g., `OPENAI_API_KEY`, `JWT_SECRET`).

### Docker Setup (Recommended)

To run the full environment (App + Local DB) immediately:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:5000`.

### Local Development Setup

If you prefer to run without Docker:

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application:
    ```bash
    python run.py
    ```

## Architecture Overview

The backend is a RESTful API built with Flask. It uses SQLAlchemy for database interactions with a SQLite database. Authentication is handled via JWT tokens. The application is containerized using Docker for consistent deployment.
