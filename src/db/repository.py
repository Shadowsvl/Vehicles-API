from typing import List, Optional
from pymongo.database import Database
from pymongo.results import InsertOneResult, UpdateResult, DeleteResult
from bson import ObjectId
from src.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate

class VehicleRepository:
    def __init__(self, db: Database):
        self.collection = db.get_collection("vehicles")

    def create(self, vehicle: VehicleCreate) -> Vehicle:
        vehicle_dict = vehicle.model_dump(by_alias=True, exclude=["id"])
        self._convert_dates(vehicle_dict)
        result: InsertOneResult = self.collection.insert_one(vehicle_dict)
        return Vehicle(id=str(result.inserted_id), **vehicle.model_dump())
    
    def _convert_dates(self, data: dict):
        from datetime import date, datetime
        for key, value in data.items():
            if isinstance(value, date) and not isinstance(value, datetime):
                data[key] = datetime.combine(value, datetime.min.time())


    def get_by_id(self, vehicle_id: str) -> Optional[Vehicle]:
        if not ObjectId.is_valid(vehicle_id):
            return None
        
        doc = self.collection.find_one({"_id": ObjectId(vehicle_id)})
        if doc:
            return Vehicle(**doc)
        return None

    def get_by_field(self, field: str, value: str) -> Optional[Vehicle]:
        doc = self.collection.find_one({field: value})
        if doc:
            return Vehicle(**doc)
        return None


    def list(self, skip: int = 0, limit: int = 100) -> List[Vehicle]:
        cursor = self.collection.find().skip(skip).limit(limit)
        return [Vehicle(**doc) for doc in cursor]

    def update(self, vehicle_id: str, vehicle_update: VehicleUpdate) -> Optional[Vehicle]:
        if not ObjectId.is_valid(vehicle_id):
            return None
        
        # Filter out None values to only update provided fields
        update_data = vehicle_update.model_dump(by_alias=True, exclude_unset=True)
        self._convert_dates(update_data)
        
        if not update_data:
            return self.get_by_id(vehicle_id)

        result: UpdateResult = self.collection.find_one_and_update(
            {"_id": ObjectId(vehicle_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            return Vehicle(**result)
        return None

    def delete(self, vehicle_id: str) -> bool:
        if not ObjectId.is_valid(vehicle_id):
            return False
        
        result: DeleteResult = self.collection.delete_one({"_id": ObjectId(vehicle_id)})
        return result.deleted_count > 0
