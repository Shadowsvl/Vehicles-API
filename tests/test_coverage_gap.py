import pytest
from unittest.mock import patch, MagicMock
from src.db.database import DatabaseManager, get_database
from src.services.vehicle_service import VehicleService
from src.models.vehicle import Vehicle, VehicleCreate, VehicleUpdate, VehicleType
from fastapi import HTTPException
from src.api.deps import get_repository, get_service

# --- Database Manager Tests ---
def test_database_manager_connect():
    with patch("src.db.database.MongoClient") as mock_client:
        DatabaseManager.client = None # Reset
        DatabaseManager.connect()
        mock_client.assert_called_once()
        assert DatabaseManager.client is not None
        
        # Test get_db lazy connect
        DatabaseManager.client = None
        db = DatabaseManager.get_db()
        assert db is not None
        assert mock_client.call_count == 2
        
        # Test close
        with patch("builtins.print") as mock_print:
            DatabaseManager.close()
            mock_client.return_value.close.assert_called()

def test_get_database_dependency():
    with patch("src.db.database.DatabaseManager.get_db") as mock_get:
        get_database()
        mock_get.assert_called_once()


# --- Dependency Tests ---
def test_dependencies():
    mock_db = MagicMock()
    repo = get_repository(mock_db)
    assert repo.collection is not None
    
    service = get_service(repo)
    assert service.repository is repo
    

# --- Service Edge Case Tests ---
@pytest.fixture
def mock_repo():
    return MagicMock()

@pytest.fixture
def service(mock_repo):
    return VehicleService(mock_repo)

def test_service_delete_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.delete_vehicle("bad_id")
    assert exc.value.status_code == 404

def test_service_update_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.update_vehicle("bad_id", VehicleUpdate())
    assert exc.value.status_code == 404

def test_service_update_duplicate_placa(service, mock_repo):
    # Original vehicle
    mock_repo.get_by_id.return_value = Vehicle(
        _id="123", 
        placa="AA-100-AA", 
        numero_economico="1", 
        marca="Volvo", 
        modelo="VNL", 
        anno=2020, 
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK, 
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567", 
        poliza_seguro="p", 
        vigencia_seguro="2020-01-01"
    )
    # Existing other vehicle
    mock_repo.get_by_field.return_value = Vehicle(
        _id="456", 
        placa="BB-200-BB", 
        numero_economico="2", 
        marca="Volvo", 
        modelo="VNL", 
        anno=2020, 
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK, 
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567", 
        poliza_seguro="p", 
        vigencia_seguro="2020-01-01"
    )
    
    with pytest.raises(HTTPException) as exc:
        service.update_vehicle("123", VehicleUpdate(placa="BB-200-BB"))
    assert exc.value.status_code == 400
    assert "license plate already exists" in exc.value.detail

def test_service_update_duplicate_economico(service, mock_repo):
    mock_repo.get_by_id.return_value = Vehicle(
        _id="123", 
        placa="AA-100-AA", 
        numero_economico="1", 
        marca="Volvo", 
        modelo="VNL", 
        anno=2020, 
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK, 
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567", 
        poliza_seguro="p", 
        vigencia_seguro="2020-01-01"
    )
    mock_repo.get_by_field.return_value = Vehicle(
        _id="456", 
        placa="BB-200-BB", 
        numero_economico="2", 
        marca="Volvo", 
        modelo="VNL", 
        anno=2020, 
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK, 
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567", 
        poliza_seguro="p", 
        vigencia_seguro="2020-01-01"
    )
    
    with pytest.raises(HTTPException) as exc:
        service.update_vehicle("123", VehicleUpdate(numero_economico="2"))
    assert exc.value.status_code == 400
    assert "fleet number already exists" in exc.value.detail

def test_service_get_not_found(service, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(HTTPException) as exc:
        service.get_vehicle("bad_id")
    assert exc.value.status_code == 404

def test_service_create_duplicate_economico(service, mock_repo):
    # Pass placa check
    mock_repo.get_by_field.side_effect = [None, True, None] # plaque ok, econ exists
    
    with pytest.raises(HTTPException) as exc:
        service.create_vehicle(MagicMock(placa="AA-100-AA", numero_economico="e", numero_serie="s"))
    assert exc.value.status_code == 400
    assert "fleet number" in exc.value.detail

def test_service_create_duplicate_vin(service, mock_repo):
    # Pass placa, econ check
    mock_repo.get_by_field.side_effect = [None, None, True]
    
    with pytest.raises(HTTPException) as exc:
        service.create_vehicle(MagicMock(placa="AA-100-AA", numero_economico="e", numero_serie="s"))
    assert exc.value.status_code == 400
    assert "VIN" in exc.value.detail

def test_service_update_fail_db(service, mock_repo):
     mock_repo.get_by_id.return_value = Vehicle(
        _id="123", 
        placa="AA-100-AA", 
        numero_economico="1", 
        marca="Volvo", 
        modelo="VNL", 
        anno=2020, 
        tipo_vehiculo=VehicleType.TRACTOR_TRUCK, 
        capacidad_carga_kg=20000, 
        numero_serie="12345678901234567", 
        poliza_seguro="p", 
        vigencia_seguro="2020-01-01"
    )
     mock_repo.get_by_field.return_value = None
     mock_repo.update.return_value = None # DB Update failed for some reason
     
     with pytest.raises(HTTPException) as exc:
         service.update_vehicle("123", VehicleUpdate(placa="New"))
     assert exc.value.status_code == 404
