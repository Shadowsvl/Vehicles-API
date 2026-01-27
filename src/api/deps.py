from typing import Annotated
from fastapi import Depends
from pymongo.database import Database
from src.db.database import get_database
from src.db.repository import VehicleRepository
from src.services.vehicle_service import VehicleService

def get_repository(db: Annotated[Database, Depends(get_database)]) -> VehicleRepository:
    return VehicleRepository(db)

def get_service(repository: Annotated[VehicleRepository, Depends(get_repository)]) -> VehicleService:
    return VehicleService(repository)
