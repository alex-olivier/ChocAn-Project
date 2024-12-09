import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from chocan_software.models import Base, Member, Provider, Service, ServiceRecord
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.person_manager import MemberManager, ProviderManager
from chocan_software.data_managers.service_manager import ServiceManager
from chocan_software.service_record_manager import ServiceRecordManager

# Test database URL
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_manager():
    """Fixture to provide a test DatabaseManager instance with an in-memory database."""
    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.create_all(engine)
    db_manager = DatabaseManager(engine)
    yield db_manager
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def session(db_manager):
    """Fixture to provide a fresh session for each test."""
    with db_manager.get_session(commit=True) as session:
        yield session

def test_add_member(db_manager):
    """Test adding a member."""
    member_manager = MemberManager(db_manager)
    member_manager.add_member(
        name="John Doe",
        street_address="123 Elm St",
        city="Springfield",
        state="IL",
        zip_code="62704"
    )
    with db_manager.get_session() as session:
        member = session.query(Member).filter_by(name="John Doe").first()
        assert member is not None
        assert member.city == "Springfield"

def test_add_provider(db_manager):
    """Test adding a provider."""
    provider_manager = ProviderManager(db_manager)
    provider_manager.add_provider(
        name="Jane Smith",
        street_address="456 Maple Ave",
        city="Metropolis",
        state="NY",
        zip_code="10001"
    )
    with db_manager.get_session() as session:
        provider = session.query(Provider).filter_by(name="Jane Smith").first()
        assert provider is not None
        assert provider.state == "NY"

def test_add_service(db_manager):
    """Test adding a service."""
    service_manager = ServiceManager(db_manager)
    service_manager.add_service(name="Massage Therapy", fee=75.00)
    with db_manager.get_session() as session:
        service = session.query(Service).filter_by(name="Massage Therapy").first()
        assert service is not None
        assert service.fee == 75.00

def test_create_service_record(db_manager, session):
    """Test creating a service record."""
    # Add sample data
    member = Member(
        name="John Doe",
        street_address="123 Elm St",
        city="Springfield",
        state="IL",
        zip_code="62704",
        status=True
    )
    provider = Provider(
        name="Jane Smith",
        street_address="456 Maple Ave",
        city="Metropolis",
        state="NY",
        zip_code="10001"
    )
    service = Service(name="Massage Therapy", fee=75.00)
    session.add_all([member, provider, service])
    session.commit()

    # Create service record
    service_record_manager = ServiceRecordManager(db_manager)
    service_record_manager.add_service_record(
        provider_number=provider.id,
        member_number=member.id,
        service_code=service.id,
        date_of_service="12-01-2024",
        comments="Great session!"
    )

    # Validate service record
    service_record = session.query(ServiceRecord).first()
    assert service_record is not None
    assert service_record.comments == "Great session!"

def test_view_services(db_manager, capsys):
    """Test viewing services."""
    service_manager = ServiceManager(db_manager)
    service_manager.add_service(name="Massage Therapy", fee=75.00)
    service_manager.add_service(name="Acupuncture", fee=50.00)
    
    service_manager.view_services()
    captured = capsys.readouterr()
    assert "Massage Therapy" in captured.out
    assert "Acupuncture" in captured.out

def test_update_member(db_manager):
    """Test updating a member."""
    member_manager = MemberManager(db_manager)
    member_manager.add_member(
        name="John Doe",
        street_address="123 Elm St",
        city="Springfield",
        state="IL",
        zip_code="62704"
    )
    member_manager.update_member(
        member_number=1,
        city="Updated City"
    )
    with db_manager.get_session() as session:
        member = session.query(Member).filter_by(name="John Doe").first()
        assert member is not None
        assert member.city == "Updated City"

def test_delete_provider(db_manager):
    """Test deleting a provider."""
    provider_manager = ProviderManager(db_manager)
    provider_manager.add_provider(
        name="Jane Smith",
        street_address="456 Maple Ave",
        city="Metropolis",
        state="NY",
        zip_code="10001"
    )
    provider_manager.delete_provider(provider_number=1)
    with db_manager.get_session() as session:
        provider = session.query(Provider).filter_by(name="Jane Smith").first()
        assert provider is None
