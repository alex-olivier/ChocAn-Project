import pytest
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Member, Provider, Service, ServiceRecord, ProviderService

# Define the directory for test data
TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), "test_valid_data")

@pytest.fixture(scope="function")
def test_database():
    # Create an in-memory SQLite database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()
    Base.metadata.drop_all(engine)

def load_csv_to_table(csv_filename, model_class, session):
    """Utility function to load CSV data into a database table."""
    file_path = os.path.join(TEST_DATA_DIR, csv_filename)  # Construct the full file path
    data = pd.read_csv(file_path)
    for _, row in data.iterrows():
        record = model_class(**row.to_dict())
        session.add(record)
    session.commit()

def test_load_members(test_database):
    session = test_database
    load_csv_to_table("members.csv", Member, session)
    members = session.query(Member).all()
    assert len(members) > 0  # Ensure members are loaded
    assert all(len(m.name) <= 25 for m in members)  # Validate name length constraint

def test_load_providers(test_database):
    session = test_database
    load_csv_to_table("providers.csv", Provider, session)
    providers = session.query(Provider).all()
    assert len(providers) > 0  # Ensure providers are loaded
    assert all(len(p.name) <= 25 for p in providers)  # Validate name length constraint

def test_load_services(test_database):
    session = test_database
    load_csv_to_table("services.csv", Service, session)
    services = session.query(Service).all()
    assert len(services) > 0  # Ensure services are loaded
    assert all(0 < s.fee <= 999.99 for s in services)  # Validate fee constraint

def test_load_provider_services(test_database):
    session = test_database
    load_csv_to_table("provider_services.csv", ProviderService, session)
    provider_services = session.query(ProviderService).all()
    assert len(provider_services) > 0  # Ensure provider services are loaded

def test_load_service_records(test_database):
    session = test_database
    load_csv_to_table("service_records.csv", ServiceRecord, session)
    service_records = session.query(ServiceRecord).all()
    assert len(service_records) > 0  # Ensure service records are loaded
    assert all(r.service_date <= r.timestamp for r in service_records)  # Validate timestamps
