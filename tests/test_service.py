import pytest
from unittest.mock import Mock, MagicMock
from fastapi import HTTPException
from src.services.vehicle_service import VehicleService
from src.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate, VehicleType, VehicleStatus

@pytest.fixture
def mock_repo():
    return Mock()

@pytest.fixture
def service(mock_repo):
    return VehicleService(mock_repo)

def test_create_vehicle_success(service, mock_repo):
    # Setup
    vehicle_in = VehicleCreate(
        placa="AA-123-BB",
        numero_economico="100",
        marca="Volvo",
        modelo="VNL",
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=20000,
        numero_serie="12345678901234567",
        poliza_seguro="P-123",
        vigencia_seguro="2025-01-01"
    )
    
    # Mock no existing vehicles
    mock_repo.check_uniqueness.return_value = []
    # Mock successful creation
    created_vehicle = Vehicle(id="mock_id", **vehicle_in.model_dump())
    mock_repo.create.return_value = created_vehicle

    # Execute
    result = service.create_vehicle(vehicle_in)

    # Verify
    assert result == created_vehicle
    mock_repo.create.assert_called_once()

def test_create_vehicle_duplicate_placa(service, mock_repo):
    vehicle_in = VehicleCreate(
        placa="AA-123-BB",
        numero_economico="100",
        marca="Volvo",
        modelo="VNL",
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=20000,
        numero_serie="12345678901234567",
        poliza_seguro="P-123",
        vigencia_seguro="2025-01-01"
    )
    
    # Mock existing vehicle with same placa
    mock_repo.check_uniqueness.return_value = [Vehicle(id="existing", **vehicle_in.model_dump())]

    # Execute
    with pytest.raises(HTTPException) as exc:
        service.create_vehicle(vehicle_in)
    
    assert exc.value.status_code == 400
    assert "license plate already exists" in exc.value.detail

def test_update_vehicle_success(service, mock_repo):
    vehicle_id = "test_id"
    existing_vehicle = Vehicle(
        id=vehicle_id,
        placa="OLD-PL8",
        numero_economico="100",
        marca="Volvo", 
        modelo="VNL", 
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567",
        poliza_seguro="P-123", 
        vigencia_seguro="2025-01-01"
    )

    mock_repo.get_by_id.return_value = existing_vehicle
    mock_repo.get_by_field.return_value = None # No duplicates for new values
    
    update_data = VehicleUpdate(placa="NEW-PL8")
    updated_vehicle = existing_vehicle.model_copy(update={"placa": "NEW-PL8"})
    mock_repo.update.return_value = updated_vehicle

    result = service.update_vehicle(vehicle_id, update_data)

    assert result.placa == "NEW-PL8"
    mock_repo.update.assert_called_once()
