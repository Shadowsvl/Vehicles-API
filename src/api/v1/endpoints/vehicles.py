from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from src.services.vehicle_service import VehicleService
from src.api.deps import get_service

router = APIRouter()

@router.post("/", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(
    service: Annotated[VehicleService, Depends(get_service)],
    vehicle: VehicleCreate
):
    """
    Create a new vehicle.
    """
    return service.create_vehicle(vehicle)

@router.get("/", response_model=List[Vehicle])
def list_vehicles(
    service: Annotated[VehicleService, Depends(get_service)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
):
    """
    List vehicles with pagination.
    """
    return service.list_vehicles(skip=skip, limit=limit)

@router.get("/{vehicle_id}", response_model=Vehicle)
def get_vehicle(
    vehicle_id: str,
    service: Annotated[VehicleService, Depends(get_service)]
):
    """
    Get a specific vehicle by ID.
    """
    return service.get_vehicle(vehicle_id)

@router.put("/{vehicle_id}", response_model=Vehicle)
def update_vehicle(
    vehicle_id: str,
    vehicle_update: VehicleUpdate,
    service: Annotated[VehicleService, Depends(get_service)]
):
    """
    Update a vehicle's fields.
    """
    return service.update_vehicle(vehicle_id, vehicle_update)

@router.delete("/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(
    vehicle_id: str,
    service: Annotated[VehicleService, Depends(get_service)]
):
    """
    Delete a vehicle.
    """
    service.delete_vehicle(vehicle_id)
