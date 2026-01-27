import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
from src.main import app
from src.services.vehicle_service import VehicleService
from src.models.vehicle import Vehicle, VehicleCreate, VehicleType, VehicleStatus
from src.api.deps import get_service
from src.db.database import DatabaseManager

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_db_connection():
    """Mock DB connection to prevent startup connection attempts."""
    with patch.object(DatabaseManager, 'connect'), patch.object(DatabaseManager, 'close'):
        yield

@pytest.fixture
def mock_service():
    """Create a mock service and setup dependency override."""
    service_mock = MagicMock(spec=VehicleService)
    app.dependency_overrides[get_service] = lambda: service_mock
    yield service_mock
    app.dependency_overrides = {}

def test_create_vehicle_api(mock_service):
    vehicle_data = {
        "placa": "AA-123-BB",
        "numero_economico": "100",
        "marca": "Kenworth",
        "modelo": "T680",
        "anno": 2023,
        "tipo_vehiculo": "TRACTOR_TRUCK",
        "capacidad_carga_kg": 20000,
        "numero_serie": "12345678901234567",
        "poliza_seguro": "P-123",
        "vigencia_seguro": "2025-12-31"
    }
    
    # Mock return value
    created_vehicle = Vehicle(id="123", **vehicle_data)
    mock_service.create_vehicle.return_value = created_vehicle

    response = client.post("/api/v1/vehicles/", json=vehicle_data)
    
    assert response.status_code == 201
    assert response.json()["id"] == "123"
    assert response.json()["placa"] == "AA-123-BB"
    mock_service.create_vehicle.assert_called_once()

def test_get_vehicle_api(mock_service):
    vehicle_id = "123"
    vehicle = Vehicle(
        id=vehicle_id,
        placa="AA-123-BB",
        numero_economico="100",
        marca="Kenworth",
        modelo="T680",
        anno=2023,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=20000,
        numero_serie="12345678901234567",
        poliza_seguro="P-123",
        vigencia_seguro="2025-12-31"
    )
    mock_service.get_vehicle.return_value = vehicle

    response = client.get(f"/api/v1/vehicles/{vehicle_id}")
    
    assert response.status_code == 200
    assert response.json()["id"] == vehicle_id

def test_get_vehicle_not_found(mock_service):
    from fastapi import HTTPException
    mock_service.get_vehicle.side_effect = HTTPException(status_code=404, detail="Vehicle not found")
    
    response = client.get("/api/v1/vehicles/unknown")
    
    assert response.status_code == 404
    assert response.json()["error"]["message"] == "Vehicle not found"

def test_list_vehicles_api(mock_service):
    mock_service.list_vehicles.return_value = []
    
    response = client.get("/api/v1/vehicles/?skip=0&limit=10")
    
    assert response.status_code == 200
    assert response.json() == []
    mock_service.list_vehicles.assert_called_with(skip=0, limit=10)

def test_docs_endpoint():
    response = client.get("/docs")
    assert response.status_code == 200
