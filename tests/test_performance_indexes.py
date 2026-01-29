import pytest
from mongomock import MongoClient
from src.db.repository import VehicleRepository

@pytest.fixture
def mock_db():
    client = MongoClient()
    return client.db

def test_indexes_are_created(mock_db):
    repo = VehicleRepository(mock_db)

    # This method is expected to be added
    repo.create_indexes()

    indexes = repo.collection.index_information()

    # Check for 'placa' index
    # index_information returns a dict where keys are index names and values are index details
    # We can verify by checking if there's an index with key 'placa'

    placa_index_found = False
    numero_economico_index_found = False
    numero_serie_index_found = False

    for index_name, index_info in indexes.items():
        keys = index_info['key'] # list of tuples
        unique = index_info.get('unique', False)

        # keys is like [('placa', 1)]
        if keys == [('placa', 1)]:
            placa_index_found = True
            assert unique is True, "placa index should be unique"

        if keys == [('numero_economico', 1)]:
            numero_economico_index_found = True
            assert unique is True, "numero_economico index should be unique"

        if keys == [('numero_serie', 1)]:
            numero_serie_index_found = True
            assert unique is True, "numero_serie index should be unique"

    assert placa_index_found, "Index for 'placa' not found"
    assert numero_economico_index_found, "Index for 'numero_economico' not found"
    assert numero_serie_index_found, "Index for 'numero_serie' not found"
