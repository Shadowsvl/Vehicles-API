from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.db.database import DatabaseManager
from src.db.repository import VehicleRepository
from src.api.v1.endpoints import vehicles

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    DatabaseManager.connect()
    repo = VehicleRepository(DatabaseManager.get_db())
    repo.create_indexes()
    yield
    # Shutdown
    DatabaseManager.close()

app = FastAPI(
    title="Vehicles API",
    description="API for managing vehicle fleet",
    version="1.0.0",
    lifespan=lifespan
)

# Global Exception Handler
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail,
            }
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Validation error",
                "details": exc.errors(),
            }
        },
    )

app.include_router(vehicles.router, prefix="/api/v1/vehicles", tags=["vehicles"])

@app.get("/health", status_code=200)
async def health_check() -> dict[str, str]:
    """
    Health check endpoint to verify service status.
    """
    return {"status": "ok"}
