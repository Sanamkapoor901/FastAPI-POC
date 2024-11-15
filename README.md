# FastAPI Project Setup

## Prerequisites
- Docker and Docker Compose
- Python 3.10+

## Setup Steps

1. Clone the repository
2. Create a `.env` file with the following variables:
    ```
    cp sample.env .env
    ```
3. Run `docker compose up --build` to start the services.
4. Run `docker compose up --build -d` to start the services in detached mode.
5. The API will be available at `http://localhost:8000`.

## Running Tests
Run `docker compose exec web pytest` to run the tests.