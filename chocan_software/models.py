# from sqlalchemy import (
#     Column, Integer, String, Float, Boolean, CheckConstraint, UniqueConstraint, 
#     ForeignKey, DateTime, func
# )
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy import UniqueConstraint
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.orm import relationship
from chocan_software.constants import (
    NAME_MAX_LEN, STREET_ADDRESS_MAX_LEN, CITY_MAX_LEN, STATE_LEN, ZIP_CODE_LEN,
    MEMBER_STATUS_ACTIVE, SERVICE_NAME_MAX_LEN, SERVICE_FEE_MAX, SERVICERECORD_COMMENT_MAX_LEN
)
# This SQLAlchemy ORM syntax is now deprecated as of version 2.0
# from sqlalchemy.ext.declarative import declarative_base  
# Base = declarative_base()


class Base(DeclarativeBase):
    pass

class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(NAME_MAX_LEN), nullable=False)
    street_address = Column(String(STREET_ADDRESS_MAX_LEN), nullable=False)
    city = Column(String(CITY_MAX_LEN), nullable=False)
    state = Column(String(STATE_LEN), nullable=False)
    zip_code = Column(String(ZIP_CODE_LEN), nullable=False)
    status = Column(Boolean, nullable=False)

    service_records = relationship('ServiceRecord', back_populates='member')

    __table_args__ = (
        CheckConstraint(f"length(name) <= {NAME_MAX_LEN}", name="check_name_length"),
        CheckConstraint(f"length(street_address) <= {STREET_ADDRESS_MAX_LEN}", name="check_street_address_length"),
        CheckConstraint(f"length(city) <= {CITY_MAX_LEN}", name="check_city_length"),
        CheckConstraint(f"length(state) = {STATE_LEN} AND state GLOB '[A-Z]*'", name="check_state_format"),
        CheckConstraint(f"length(zip_code) = {ZIP_CODE_LEN} AND zip_code GLOB '[0-9]*'", name="check_zip_code_format"),
        CheckConstraint("status IN (0, 1)", name="check_status_boolean"),
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_member'),
    )

    def __repr__(self) -> str:
        return (
            f"Member(number={self.id:09}, "
            f"name={self.name!r}, "
            f"street_address={self.street_address!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"zip_code={self.zip_code!r}, "
            f"status={self.status!r})"
        )

    def __init__(self, name, street_address, city, state, zip_code, status=None):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.status = status if status is not None else MEMBER_STATUS_ACTIVE
    

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(NAME_MAX_LEN), nullable=False)
    street_address = Column(String(STREET_ADDRESS_MAX_LEN), nullable=False)
    city = Column(String(CITY_MAX_LEN), nullable=False)
    state = Column(String(STATE_LEN), nullable=False)
    zip_code = Column(String(ZIP_CODE_LEN), nullable=False)

    service_records = relationship('ServiceRecord', back_populates='provider')
    provider_services = relationship('ProviderService', back_populates='provider')

    __table_args__ = (
        CheckConstraint(f"length(name) <= {NAME_MAX_LEN}", name="check_name_length"),
        CheckConstraint(f"length(street_address) <= {STREET_ADDRESS_MAX_LEN}", name="check_street_address_length"),
        CheckConstraint(f"length(city) <= {CITY_MAX_LEN}", name="check_city_length"),
        CheckConstraint(f"length(state) = {STATE_LEN} AND state GLOB '[A-Z]*'", name="check_state_format"),
        CheckConstraint(f"length(zip_code) = {ZIP_CODE_LEN} AND zip_code GLOB '[0-9]*'", name="check_zip_code_format"),
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_provider'),
    )

    def __repr__(self) -> str:
        return (
            f"Provider(number={self.id:09}, "
            f"name={self.name!r}, "
            f"street_address={self.street_address!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"zip_code={self.zip_code!r})"
        )
    
    def __init__(self, name, street_address, city, state, zip_code):
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(SERVICE_NAME_MAX_LEN), nullable=False)
    fee = Column(Float, nullable=False)

    provider_services = relationship('ProviderService', back_populates='service')
    service_records = relationship('ServiceRecord', back_populates='service')
    
    __table_args__ = (
        CheckConstraint(f"length(name) <= {SERVICE_NAME_MAX_LEN}", name="check_service_name_length"),
        CheckConstraint(f"fee < {SERVICE_FEE_MAX}", name="check_service_fee_limit"),
        UniqueConstraint('name', 'fee', name='unique_service'),
    )
    
    def __repr__(self) -> str:
        return (
            f"Service(code={self.id:06}, "
            f"name={self.name!r}, "
            f"fee={self.fee!r})"
        )


class ProviderService(Base):
    __tablename__ = 'provider_services'

    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    
    provider = relationship('Provider', back_populates='provider_services')
    service = relationship('Service', back_populates='provider_services')


class ServiceRecord(Base):
    __tablename__ = 'service_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    service_date = Column(DateTime, nullable=False)  # Use DateTime for service_date
    timestamp = Column(DateTime, nullable=False, default=func.now())  # Automatically generate timestamp
    comments = Column(String(SERVICERECORD_COMMENT_MAX_LEN))

    provider = relationship('Provider', back_populates='service_records')
    member = relationship('Member', back_populates='service_records')
    service = relationship('Service', back_populates='service_records')

    __table_args__ = (
        CheckConstraint(f"length(comments) <= {SERVICERECORD_COMMENT_MAX_LEN}", name="check_comments_length"),
        CheckConstraint("service_date <= CURRENT_TIMESTAMP", name="check_service_date_not_future"),
        UniqueConstraint('provider_id', 'member_id', 'service_id', 'service_date', name='unique_service_record'),
    )

    def __repr__(self) -> str:
        return (
            f"ServiceRecord(provider_id={self.provider_id:09}, "
            f"member_id={self.member_id:09}, "
            f"service_id={self.service_id:06}, "
            f"service_date={self.service_date!r}, "
            f"timestamp={self.timestamp!r}, "
            f"comments={self.comments!r})"
        )
