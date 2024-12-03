from sqlalchemy import (
    Column, 
    Integer, 
    String, 
    Float,
    Boolean,
    CheckConstraint, 
    UniqueConstraint, 
    ForeignKey, 
    DateTime, 
    func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from constants import (
    TYPE_MAX_LEN,
    NUMBER_LEN,
    NAME_MAX_LEN, 
    STREET_ADDRESS_MAX_LEN, 
    CITY_MAX_LEN, 
    STATE_LEN, 
    ZIP_CODE_LEN,
    SERVICE_CODE_LEN,
    SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX,
    COMMENT_MAX_LEN
)
# from sqlalchemy.event import listens_for

Base = declarative_base()

class Person(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(NAME_MAX_LEN), nullable=False)
    street_address = Column(String(STREET_ADDRESS_MAX_LEN), nullable=False)
    city = Column(String(CITY_MAX_LEN), nullable=False)
    state = Column(String(STATE_LEN), nullable=False)
    zip_code = Column(String(ZIP_CODE_LEN), nullable=False)
    number = Column(String(NUMBER_LEN), nullable=True)
    type = Column(String(TYPE_MAX_LEN))

    __table_args__ = (
        CheckConstraint(f"length(name) <= {NAME_MAX_LEN}", name="check_name_length"),
        CheckConstraint(f"length(street_address) <= {STREET_ADDRESS_MAX_LEN}", name="check_street_address_length"),
        CheckConstraint(f"length(city) <= {CITY_MAX_LEN}", name="check_city_length"),
        CheckConstraint(f"length(state) = {STATE_LEN} AND state GLOB '[A-Z]*'", name="check_state_format"),
        CheckConstraint(f"length(zip_code) = {ZIP_CODE_LEN} AND zip_code GLOB '[0-9]*'", name="check_zip_code_format"),
        UniqueConstraint('number', 'type', name='unique_person'),
    )

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'person'
    }

    def __repr__(self):
        return ("{self.__class__.__name__}(name='{self.name}', " \
                "street_address='{self.street_address}', " \
                "city='{self.city}', state='{self.state}', " \
                "zip_code='{self.zip_code}', " \
                "number='{self.number}')").format(self=self)


class Member(Person):
    __tablename__ = 'members'

    is_active = Column(Boolean, nullable=False)
    
    service_records = relationship('ServiceRecord', back_populates='member')

    __table_args__ = (
        CheckConstraint("is_active IN (0, 1)", name="check_is_active_boolean"),
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_member'),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'member'
    }

    def __repr__(self):
        parent_repr = super().__repr__()
        return parent_repr[:-1] + f", is_active={self.is_active})"


class Provider(Person):
    __tablename__ = 'providers'

    service_records = relationship('ServiceRecord', back_populates='provider')
    provider_services = relationship('ProviderService', back_populates='provider')

    __table_args__ = (
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_provider'),
    )

    __mapper_args__ = {
        'polymorphic_identity': 'provider'
    }


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(SERVICE_CODE_LEN), unique=True, nullable=True)
    name = Column(String(SERVICE_NAME_MAX_LEN), nullable=False)
    fee = Column(Float, nullable=False)
    
    provider_services = relationship('ProviderService', back_populates='service')
    service_records = relationship('ServiceRecord', back_populates='service')

    __table_args__ = (
        CheckConstraint(f"length(name) <= {SERVICE_NAME_MAX_LEN}", name="check_service_name_length"),
        CheckConstraint(f"fee < {SERVICE_FEE_MAX}", name="check_service_fee_limit"),
        UniqueConstraint('name', 'fee', name='unique_service'),
    )

    def __repr__(self):
        return ("{self.__class__.__name__}(code='{self.code}', " \
                "name='{self.name}', " \
                "fee={self.fee})").format(self=self)


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
    date_of_service = Column(DateTime, nullable=False)  # Use DateTime for date_of_service
    timestamp = Column(DateTime, nullable=False, default=func.now())  # Automatically generate timestamp
    comments = Column(String(COMMENT_MAX_LEN))

    provider = relationship('Provider', back_populates='service_records')
    member = relationship('Member', back_populates='service_records')
    service = relationship('Service', back_populates='service_records')


    __table_args__ = (
        CheckConstraint(f"length(comments) <= {COMMENT_MAX_LEN}", name="check_comments_length"),
        CheckConstraint("date_of_service <= CURRENT_TIMESTAMP", name="check_date_of_service_not_future"),
        UniqueConstraint('provider_id', 'member_id', 'service_id', 'date_of_service', name='unique_service_record'),
    )