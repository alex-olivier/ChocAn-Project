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
    if len(target.name) > 25:
        raise ValueError("Name must be up to 25 characters.")
    if len(target.street_address) > 25:
        raise ValueError("Street address must be up to 25 characters.")
    if len(target.city) > 14:
        raise ValueError("City must be up to 14 characters.")
    if not (len(target.state) == 2 and target.state.isupper()):
        raise ValueError("State must include 2 uppercase letters.")
    if not (len(target.zip_code) == 5 and target.zip_code.isdigit()):
        raise ValueError("Zip code must include 5 digits.")

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
            target.__table__
            .update().where(
                target.__table__.c.id == target.id
            ).values(
                number=target.number
            )
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