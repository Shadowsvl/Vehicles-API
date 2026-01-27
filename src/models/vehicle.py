from datetime import date, datetime
from enum import Enum
from typing import Annotated, Optional
import re

from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_validator

# Helper for MongoDB ObjectId
PyObjectId = Annotated[str, BeforeValidator(str)]

class VehicleType(str, Enum):
    TRACTOR_TRUCK = "TRACTOR_TRUCK"
    RIGID_TRUCK = "RIGID_TRUCK"
    TRAILER = "TRAILER"
    DOLLY = "DOLLY"

class VehicleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    IN_MAINTENANCE = "IN_MAINTENANCE"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class FuelType(str, Enum):
    DIESEL = "DIESEL"
    NATURAL_GAS = "NATURAL_GAS"
    ELECTRIC = "ELECTRIC"

class VehicleBase(BaseModel):
    placa: str = Field(..., description="Mexican license plate", min_length=6, max_length=10)
    numero_economico: str = Field(..., description="Internal fleet number")
    marca: str = Field(..., description="Vehicle brand")
    modelo: str = Field(..., description="Vehicle model")
    anno: int = Field(..., ge=1990, description="Year of manufacture")
    tipo_vehiculo: VehicleType
    capacidad_carga_kg: float = Field(..., gt=0, description="Load capacity in kg")
    numero_serie: str = Field(..., min_length=17, max_length=17, description="VIN")
    estado_vehiculo: VehicleStatus = VehicleStatus.ACTIVE
    fecha_alta: datetime = Field(default_factory=datetime.utcnow)
    ultima_verificacion: Optional[datetime] = None
    poliza_seguro: str
    vigencia_seguro: date

    # Optional attributes
    kilometraje_actual: Optional[int] = None
    tipo_combustible: Optional[FuelType] = None
    rendimiento_km_litro: Optional[float] = None
    gps_id: Optional[str] = None
    base_operativa: Optional[str] = None

    @field_validator('placa')
    @classmethod
    def validate_placa(cls, v: str) -> str:
        # Mexican Federal Transport plates often follow patterns, but variations exist.
        # Strict validation example: 2-3 letters, hyphen, 4-6 digits or similar alphanumeric combos.
        # We will use a regex that permits common formats (e.g. "AA-1234", "12-AA-3A", etc) 
        # but enforces uppercase and no special chars other than hyphen.
        upper_v = v.upper()
        if not re.match(r'^[A-Z0-9]{2,4}-?[A-Z0-9]{2,7}(?:-[A-Z0-9]{1,3})?$', upper_v):
             raise ValueError('Invalid Mexican license plate format. Expected uppercase alphanumeric (e.g., AB-12345)')
        return upper_v

    model_config = ConfigDict(
        populate_by_name=True,
        json_schema_extra={
            "example": {
                "placa": "AB-123-CD",
                "numero_economico": "FLEET-001",
                "marca": "Kenworth",
                "modelo": "T680",
                "anno": 2023,
                "tipo_vehiculo": "TRACTOR_TRUCK",
                "capacidad_carga_kg": 20000.0,
                "numero_serie": "1M8GDM9A_KP042788", # 17 chars
                "estado_vehiculo": "ACTIVE",
                "poliza_seguro": "POL-987654321",
                "vigencia_seguro": "2025-12-31"
            }
        }
    )

class VehicleCreate(VehicleBase):
    pass

class VehicleUpdate(BaseModel):
    """Fields that can be updated"""
    placa: Optional[str] = None
    numero_economico: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anno: Optional[int] = Field(None, ge=1990)
    tipo_vehiculo: Optional[VehicleType] = None
    capacidad_carga_kg: Optional[float] = Field(None, gt=0)
    numero_serie: Optional[str] = Field(None, min_length=17, max_length=17)
    estado_vehiculo: Optional[VehicleStatus] = None
    ultima_verificacion: Optional[datetime] = None
    poliza_seguro: Optional[str] = None
    vigencia_seguro: Optional[date] = None
    
    # Optional attributes
    kilometraje_actual: Optional[int] = None
    tipo_combustible: Optional[FuelType] = None
    rendimiento_km_litro: Optional[float] = None
    gps_id: Optional[str] = None
    base_operativa: Optional[str] = None

    model_config = ConfigDict(populate_by_name=True)

class Vehicle(VehicleBase):
    id: Optional[PyObjectId] = Field(validation_alias="_id", default=None)
