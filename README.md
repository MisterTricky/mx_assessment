# SA ID Number Validator and Holiday Checker

A modern web application that validates South African ID numbers and checks for public holidays on birth dates. The project consists of a FastAPI backend and a Nuxt.js frontend, providing a seamless user experience for ID validation and holiday checking services. (Note: A Django version of this can also be provided, but this version uses a FastAPI backend and Nuxt.js frontend for a more modern and responsive user experience.)

## Features
- SA ID number validation and information decoding
  - Birth date extraction
  - Gender determination
  - Citizenship status
- Public holiday checking using Calendarific API
- Search history tracking
- Modern, responsive user interface
- RESTful API backend
- Swagger documentation

## Project Structure
```
├── backend/          # FastAPI backend application
│   ├── db/          # Database configurations and models
│   ├── services/    # External services integration
│   └── web/         # API endpoints and server configuration
├── frontend/        # Nuxt.js frontend application
│   ├── components/  # Reusable Vue components
│   ├── pages/       # Application pages
│   └── stores/      # State management
```

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Create a `.env` file in the backend directory with the following variables:
```bash
BACKEND_RELOAD="True"
BACKEND_PORT="8000"
BACKEND_ENVIRONMENT="dev"
BACKEND_CALENDARIFIC_API_KEY="your_api_key_here"
```

4. Start the backend server:
```bash
poetry run python -m backend
```

The backend API will be available at `http://localhost:8000` with Swagger documentation at `/api/docs`.

### Alternative: Using Docker

You can also run the backend using Docker:

```bash
cd backend
docker-compose up --build
```

For development with auto-reload:
```bash
docker-compose -f docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
```

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend application will be available at `http://localhost:3000`.

### Production Build

To build the frontend for production:
```bash
npm run build
```

## Development Tools

### Pre-commit Hooks
The backend uses pre-commit hooks for code quality. To install:
```bash
cd backend
pre-commit install
```

This will run the following checks before each commit:
- black (code formatting)
- mypy (type checking)
- ruff (linting)

## Testing

To run backend tests:
```bash
cd backend
docker-compose run --build --rm api pytest -vv .
docker-compose down
```

For local testing, start a Postgres database:
```bash
docker run -p "5432:5432" -e "POSTGRES_PASSWORD=backend" -e "POSTGRES_USER=backend" -e "POSTGRES_DB=backend" postgres:16.3-bullseye
```

Then run the tests:
```bash
pytest -vv .
