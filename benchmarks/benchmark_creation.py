import time
import sys
import os
from unittest.mock import MagicMock

# Add src to path
sys.path.append(os.getcwd())

from src.services.vehicle_service import VehicleService
from src.models.vehicle import VehicleCreate, VehicleType

def benchmark_create():
    print("Benchmarking create_vehicle (Optimized)...")

    # Mock Repository
    repo = MagicMock()

    # Simulate DB latency for the new optimized call
    # 10ms for a single query checking all 3 fields
    def check_uniqueness_side_effect(placa, numero_economico, numero_serie):
        time.sleep(0.01) # 10ms latency
        return []

    repo.check_uniqueness.side_effect = check_uniqueness_side_effect
    repo.create.return_value = MagicMock()

    service = VehicleService(repo)

    # Minimal valid vehicle
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

    iterations = 50
    start_time = time.time()
    for _ in range(iterations):
        service.create_vehicle(vehicle_in)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Time taken for {iterations} creations: {total_time:.4f}s")
    print(f"Average time per creation: {total_time/iterations:.4f}s")

if __name__ == "__main__":
    benchmark_create()
