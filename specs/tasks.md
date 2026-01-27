# Project Tasks

## Phase 1: Foundation & Setup
- [x] Initialize Git repository
- [x] Create directory structure (`src/`, `src/api`, `src/core`, `src/db`, `src/models`, `src/services`, `tests/`)
- [x] Create `Dockerfile` for Python 3.11+
- [x] Create `docker-compose.yml` (FastAPI + MongoDB)
- [x] Create `requirements.txt` with dependencies
- [x] Configure `pytest`
- [x] Implement `src/main.py` (App entrypoint)
- [x] Implement `GET /health` endpoint
- [x] Verify setup with `pytest` and `docker compose up`

## Phase 2: Core Domain & Data Access
- [x] Create Enums (`VehicleType`, `VehicleStatus`, `FuelType`)
- [x] Create `Vehicle` Pydantic models (Schema) in `src/models/vehicle.py`
- [x] Implement License Plate validation logic
- [x] Implement `VehicleRepository` in `src/db/repository.py`
- [x] Test Repository with mocked Mongo

- [/] Phase 3: Service Layer & Business Logic
    - [x] Create `VehicleService` in `src/services/vehicle_service.py`
    - [x] Implement creation logic (uniqueness checks)
    - [x] Implement update logic
    - [x] Test Service layer

## Phase 4: API Presentation Layer
- [x] Implement `src/api/v1/endpoints/vehicles.py`
- [x] Add standard JSON Error Handler
- [x] Wire up routers in `main.py`
- [x] Test all endpoints

## Phase 5: Quality Assurance
- [x] Check code coverage (>90%)
- [x] Verify OpenAPI/Swagger UI
- [x] Human review of `constitution.md` adherence
