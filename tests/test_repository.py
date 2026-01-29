import pytest
from mongomock import MongoClient
from src.db.repository import VehicleRepository
from src.models.vehicle import VehicleCreate, VehicleUpdate, VehicleType

@pytest.fixture
def mock_db():
    client = MongoClient()
    return client.db

@pytest.fixture
def repository(mock_db):
    return VehicleRepository(mock_db)

def test_create_vehicle(repository):
    vehicle_in = VehicleCreate(
        placa="AB-123-CD",
        numero_economico="001",
        marca="Volvo",
        modelo="VNL",
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=25000,
        numero_serie="12345678901234567",
        poliza_seguro="INS-001",
        vigencia_seguro="2025-01-01"
    )
    created = repository.create(vehicle_in)
    assert created.id is not None
    assert created.placa == "AB-123-CD"

def test_get_vehicle(repository):
    vehicle_in = VehicleCreate(
        placa="XY-999-ZZ",
        numero_economico="002",
        marca="Kenworth",
        modelo="T680",
        anno=2022,
        tipo_vehiculo=VehicleType.RIGID_TRUCK,
        capacidad_carga_kg=15000,
        numero_serie="X2345678901234567",
        poliza_seguro="INS-002",
        vigencia_seguro="2026-01-01"
    )
    created = repository.create(vehicle_in)
    
    fetched = repository.get_by_id(str(created.id))
    assert fetched is not None
    assert fetched.numero_economico == "002"

def test_update_vehicle(repository):
    # Setup
    vehicle_in = VehicleCreate(
        placa="UP-000-DT",
        numero_economico="003",
        marca="Freightliner",
        modelo="Cascadia",
        anno=2021,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=22000,
        numero_serie="A2345678901234567",
        poliza_seguro="INS-003",
        vigencia_seguro="2025-06-01"
    )
    created = repository.create(vehicle_in)

    # Update
    update_data = VehicleUpdate(numero_economico="003-UPDATED")
    updated = repository.update(str(created.id), update_data)
    
    assert updated is not None
    assert updated.numero_economico == "003-UPDATED"
    assert updated.placa == "UP-000-DT" # Unchanged

def test_delete_vehicle(repository):
    vehicle_in = VehicleCreate(
        placa="DL-000-TE",
        numero_economico="004",
        marca="International",
        modelo="ProStar",
        anno=2019,
        tipo_vehiculo=VehicleType.TRAILER,
        capacidad_carga_kg=30000,
        numero_serie="B2345678901234567",
        poliza_seguro="INS-004",
        vigencia_seguro="2024-12-31"
    )
    created = repository.create(vehicle_in)
    
    result = repository.delete(str(created.id))
    assert result is True
    
    fetched = repository.get_by_id(str(created.id))
    assert fetched is None

def test_check_uniqueness(repository):
    # Create 2 vehicles
    v1 = VehicleCreate(
        placa="AA-111-AA",
        numero_economico="101",
        marca="Volvo",
        modelo="VNL",
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=25000,
        numero_serie="11111111111111111",
        poliza_seguro="INS-001",
        vigencia_seguro="2025-01-01"
    )
    repository.create(v1)

    v2 = VehicleCreate(
        placa="BB-222-BB",
        numero_economico="202",
        marca="Volvo",
        modelo="VNL",
        anno=2020,
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK,
        capacidad_carga_kg=25000,
        numero_serie="22222222222222222",
        poliza_seguro="INS-002",
        vigencia_seguro="2025-01-01"
    )
    repository.create(v2)

    # Check for conflict with v1's placa
    conflicts = repository.check_uniqueness("AA-111-AA", "NEW-ECO", "NEW-VIN")
    assert len(conflicts) == 1
    assert conflicts[0].placa == "AA-111-AA"

    # Check for conflict with v2's fleet number
    conflicts = repository.check_uniqueness("NEW-PLACA", "202", "NEW-VIN")
    assert len(conflicts) == 1
    assert conflicts[0].numero_economico == "202"

    # Check for conflict with both (matches v1 and v2)
    conflicts = repository.check_uniqueness("AA-111-AA", "202", "NEW-VIN")
    assert len(conflicts) == 2
