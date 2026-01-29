from typing import List, Optional
from fastapi import HTTPException
from src.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate
from src.db.repository import VehicleRepository

class VehicleService:
    def __init__(self, repository: VehicleRepository):
        self.repository = repository

    def create_vehicle(self, vehicle: VehicleCreate) -> Vehicle:
        # Uniqueness checks
        conflicts = self.repository.check_uniqueness(vehicle.placa, vehicle.numero_economico, vehicle.numero_serie)

        if conflicts:
            if any(c.placa == vehicle.placa for c in conflicts):
                raise HTTPException(status_code=400, detail="Vehicle with this license plate already exists")
            
            if any(c.numero_economico == vehicle.numero_economico for c in conflicts):
                raise HTTPException(status_code=400, detail="Vehicle with this fleet number already exists")

            if any(c.numero_serie == vehicle.numero_serie for c in conflicts):
                raise HTTPException(status_code=400, detail="Vehicle with this VIN already exists")

        return self.repository.create(vehicle)

    def get_vehicle(self, vehicle_id: str) -> Vehicle:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return vehicle

    def list_vehicles(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        return self.repository.list(skip, limit)

    def update_vehicle(self, vehicle_id: str, updates: VehicleUpdate) -> Vehicle:
        current_vehicle = self.get_vehicle(vehicle_id)
        
        # Check uniqueness if updating fields
        if updates.placa and updates.placa != current_vehicle.placa:
             if self.repository.get_by_field("placa", updates.placa):
                raise HTTPException(status_code=400, detail="Vehicle with this license plate already exists")

        if updates.numero_economico and updates.numero_economico != current_vehicle.numero_economico:
             if self.repository.get_by_field("numero_economico", updates.numero_economico):
                raise HTTPException(status_code=400, detail="Vehicle with this fleet number already exists")
        
        updated_vehicle = self.repository.update(vehicle_id, updates)
        if not updated_vehicle:
             # Should not happen given get_vehicle check, but safe guard
             raise HTTPException(status_code=404, detail="Vehicle not found")
        
        return updated_vehicle

    def delete_vehicle(self, vehicle_id: str) -> bool:
        vehicle = self.repository.get_by_id(vehicle_id)
        if not vehicle:
            raise HTTPException(status_code=404, detail="Vehicle not found")
        return self.repository.delete(vehicle_id)
