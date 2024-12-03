from models import (
    Person, 
    Member, 
    Provider, 
    Service
)
from sqlalchemy.event import listens_for

# Event listeners for before an insert is made. 
################################################
@listens_for(Member, "before_insert")
def set_member_is_active(_mapper, _connection, target):
    target.is_active = 1

# Event Listeners to perform validation in Python so errors can be 
# caught and handled before the changes are commit to the DB.
@listens_for(Person, "before_insert")
@listens_for(Person, "before_update")
def validate_person(_mapper, _connection, target):
    """
    # Example Usage for Members
    try:
        new_member = Member(name="John Member", street_address="123 Member Rd", city="Membertown", state="TX", zip_code="12345")
        session.add_member(new_member)  # Triggers validation
        session.commit()
    except ValueError as e:
        print(e)
    
    # Example Usage for Providers
    try:
        new_provider = Provider(name="Jane Provider", street_address="123 Providder St", city="Providertown", state="TX", zip_code="12345")
        session.add_provider(new_provider)  # Triggers validation
        session.commit()
    except ValueError as e:
        print(e)
    """
    if len(target.name) > 25:
        raise ValueError("Name must be 25 characters or fewer.")
    if len(target.street_address) > 25:
        raise ValueError("Street address must be 25 characters or fewer.")
    if len(target.city) > 14:
        raise ValueError("City must be 14 characters or fewer.")
    if not (len(target.state) == 2 and target.state.isupper()):
        raise ValueError("State must be a 2-character uppercase code.")
    if not (len(target.zip_code) == 5 and target.zip_code.isdigit()):
        raise ValueError("Zip code must be a 5-digit number.")
    # # Status is automatically set to 1 (True)
    # if target.status not in [0, 1]:    
    #     raise ValueError("Status must be 0 or 1.")


# Use this when a Person model is queried
#    if len(target.number) != 9:
#        raise ValueError(f"{target.type.capitalize()} number must be a 9-character number.")

# @listens_for(Person, "before_update")

    
# Event listeners for after an insert is made. 
###############################################
# After a person is inserted, the member/provider number will be generated from it's id.
@listens_for(Person, "after_insert")
def set_person_number(_mapper, connection, target):
    if target.id is not None:
        target.number = f"{target.id:09d}"
        connection.execute(
            target.__table__.update().where(target.__table__.c.id == target.id).values(number=target.number)
        )


# After a service is inserted, the service code will be generated from it's id.
@listens_for(Service, "after_insert")
def set_service_code(_mapper, connection, target):
    if target.id is not None:
        target.code = f"{target.id:06d}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(code=target.code)
        )