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
    NAME_MAX_LEN, 
    STREET_ADDRESS_MAX_LEN, 
    CITY_MAX_LEN, 
    STATE_LEN, 
    ZIP_CODE_LEN,
    MEMBER_STATUS_ACTIVE, 
    SERVICE_NAME_MAX_LEN, 
    SERVICE_FEE_MAX, 
    SERVICERECORD_COMMENT_MAX_LEN
)


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

    service_records = relationship('ServiceRecord', backref='member')

    # Delete if backref works as intended
    """
    service_records = relationship('ServiceRecord', back_populates='member')
    """

    __table_args__ = (
        CheckConstraint(f"length(name) <= {NAME_MAX_LEN}", name="check_name_length"),
        CheckConstraint(f"length(street_address) <= {STREET_ADDRESS_MAX_LEN}", name="check_street_address_length"),
        CheckConstraint(f"length(city) <= {CITY_MAX_LEN}", name="check_city_length"),
        CheckConstraint(f"length(state) = {STATE_LEN} AND state GLOB '[A-Z]*'", name="check_state_format"),
        CheckConstraint(f"length(zip_code) = {ZIP_CODE_LEN} AND zip_code GLOB '[0-9]*'", name="check_zip_code_format"),
        CheckConstraint("status IN (0, 1)", name="check_status_boolean"),
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_member'),
    )

    def __init__(self, name, street_address, city, state, zip_code, status=None):
        """
        Initializes a Member instance.
        :param name: Name of the member.
        :param street_address: Street address of the member.
        :param city: City of the member.
        :param state: State of the member.
        :param zip_code: ZIP code of the member.
        :param status: Membership status (active or inactive).
        """
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.status = status if status is not None else MEMBER_STATUS_ACTIVE

    def __repr__(self) -> str:
        """
        Provides a string representation of the Member instance.
        :return: A string with member details.
        """
        return (
            f"Member(id={self.id:09}, "
            f"name={self.name!r}, "
            f"street_address={self.street_address!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"zip_code={self.zip_code!r}, "
            f"status={self.status})"
        )
    

class Provider(Base):
    __tablename__ = 'providers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(NAME_MAX_LEN), nullable=False)
    street_address = Column(String(STREET_ADDRESS_MAX_LEN), nullable=False)
    city = Column(String(CITY_MAX_LEN), nullable=False)
    state = Column(String(STATE_LEN), nullable=False)
    zip_code = Column(String(ZIP_CODE_LEN), nullable=False)

    service_records = relationship('ServiceRecord', backref='provider')
    provider_services = relationship('ProviderService', backref='provider')

    # Delete if backref works as intended
    """
    service_records = relationship('ServiceRecord', back_populates='provider')
    provider_services = relationship('ProviderService', back_populates='provider')
    """

    __table_args__ = (
        CheckConstraint(f"length(name) <= {NAME_MAX_LEN}", name="check_name_length"),
        CheckConstraint(f"length(street_address) <= {STREET_ADDRESS_MAX_LEN}", name="check_street_address_length"),
        CheckConstraint(f"length(city) <= {CITY_MAX_LEN}", name="check_city_length"),
        CheckConstraint(f"length(state) = {STATE_LEN} AND state GLOB '[A-Z]*'", name="check_state_format"),
        CheckConstraint(f"length(zip_code) = {ZIP_CODE_LEN} AND zip_code GLOB '[0-9]*'", name="check_zip_code_format"),
        UniqueConstraint('name', 'street_address', 'city', 'state', 'zip_code', name='unique_provider'),
    )

    def __init__(self, name, street_address, city, state, zip_code):
        """
        Initializes a Provider instance.
        :param name: Name of the provider.
        :param street_address: Street address of the provider.
        :param city: City of the provider.
        :param state: State of the provider.
        :param zip_code: ZIP code of the provider.
        """
        self.name = name
        self.street_address = street_address
        self.city = city
        self.state = state
        self.zip_code = zip_code

    def __repr__(self) -> str:
        """
        Provides a string representation of the Provider instance.
        :return: A string with provider details.
        """
        return (
            f"Provider(id={self.id:09}, "
            f"name={self.name!r}, "
            f"street_address={self.street_address!r}, "
            f"city={self.city!r}, "
            f"state={self.state!r}, "
            f"zip_code={self.zip_code!r})"
        )


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(SERVICE_NAME_MAX_LEN), nullable=False)
    fee = Column(Float, nullable=False)

    service_records = relationship('ServiceRecord', backref='service')
    provider_services = relationship('ProviderService', backref='service')

    # Delete if backref works as intended
    """
    service_records = relationship('ServiceRecord', back_populates='service')
    provider_services = relationship('ProviderService', back_populates='service')
    """

    __table_args__ = (
        CheckConstraint(f"length(name) <= {SERVICE_NAME_MAX_LEN}", name="check_service_name_length"),
        CheckConstraint(f"fee < {SERVICE_FEE_MAX}", name="check_service_fee_limit"),
        UniqueConstraint('name', 'fee', name='unique_service'),
    )
    
    def __init__(self, name, fee):
        """
        Initializes a Service instance.
        :param name: Name of the service.
        :param fee: Fee for the service.
        """
        self.name = name
        self.fee = fee

    def __repr__(self) -> str:
        """
        Provides a string representation of the Service instance.
        :return: A string with service details.
        """
        return (
            f"Service(id={self.id:06}, "
            f"name={self.name!r}, "
            f"fee={self.fee:.2f})"
        )


class ProviderService(Base):
    __tablename__ = 'provider_services'

    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    
    # Delete if backref works as intended
    """
    provider = relationship('Provider', back_populates='provider_services')
    service = relationship('Service', back_populates='provider_services')
    """

    def __init__(self, provider_id, service_id):
        """
        Initializes a ProviderService instance.
        :param provider_id: ID of the provider.
        :param service_id: ID of the service.
        """
        self.provider_id = provider_id
        self.service_id = service_id
    
    def __repr__(self) -> str:
        """
        Provides a string representation of the ProviderService instance.
        :return: A string with provider and service IDs.
        """
        return (
            f"ProviderService(provider_id={self.provider_id:09}, "
            f"service_id={self.service_id:06})"
        )


class ServiceRecord(Base):
    __tablename__ = 'service_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(Integer, ForeignKey('providers.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    member_id = Column(Integer, ForeignKey('members.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    service_date = Column(DateTime, nullable=False)  # Use DateTime for service_date
    timestamp = Column(DateTime, nullable=False, default=func.now())  # Automatically generate timestamp
    comments = Column(String(SERVICERECORD_COMMENT_MAX_LEN))

    # Delete if backref works as intended
    """
    provider = relationship('Provider', back_populates='service_records')
    member = relationship('Member', back_populates='service_records')
    service = relationship('Service', back_populates='service_records')
    """

    __table_args__ = (
        CheckConstraint(f"length(comments) <= {SERVICERECORD_COMMENT_MAX_LEN}", name="check_comments_length"),
        CheckConstraint("service_date <= CURRENT_TIMESTAMP", name="check_service_date_not_future"),
        UniqueConstraint('provider_id', 'member_id', 'service_id', 'service_date', name='unique_service_record'),
    )

    def __init__(self, provider_id, member_id, service_id, service_date, timestamp=None, comments=None):
        """
        Initializes a ServiceRecord instance.
        :param provider_id: ID of the provider.
        :param member_id: ID of the member.
        :param service_id: ID of the service.
        :param service_date: Date of the service.
        :param comments: Optional comments on the service record.
        """
        self.provider_id = provider_id
        self.member_id = member_id
        self.service_id = service_id
        self.service_date = service_date
        self.timestamp = timestamp if timestamp is not None else func.now()
        self.comments = comments

    def __repr__(self) -> str:
        """
        Provides a string representation of the ServiceRecord instance.
        :return: A string with key attributes of the service record.
        """
        return (
            f"ServiceRecord(id={self.id}, "
            f"provider_id={self.provider_id:09}, "
            f"member_id={self.member_id:09}, "
            f"service_id={self.service_id:06}, "
            f"service_date={self.service_date}, "
            f"timestamp={self.timestamp}, "
            f"comments={self.comments!r})"
        )