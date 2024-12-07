from models import (
    Person, 
    Member, 
    Provider, 
    Service
)
from sqlalchemy.event import listens_for
from constants import (
    NAME_MAX_LEN, 
    STREET_ADDRESS_MAX_LEN, 
    CITY_MAX_LEN, 
    STATE_LEN, 
    ZIP_CODE_LEN,
    SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX
)

# @listens_for(Member, "before_insert")
# def set_member_is_active(_mapper, _connection, target):
#     target.is_active = True


# Event Listeners to perform validation in Python so errors can be 
# caught and handled before the changes are commit to the DB.
@listens_for(Member, "before_insert")
@listens_for(Member, "before_update")
@listens_for(Provider, "before_insert")
@listens_for(Provider, "before_update")
def validate_person(_mapper, _connection, target):
    if len(target.name) > NAME_MAX_LEN:
        raise ValueError("Name must be up to 25 characters.")
    if len(target.street_address) > STREET_ADDRESS_MAX_LEN:
        raise ValueError("Street address must be up to 25 characters.")
    if len(target.city) > CITY_MAX_LEN:
        raise ValueError("City must be up to 14 characters.")
    if not (len(target.state) == STATE_LEN and target.state.isupper()):
        raise ValueError("State must include 2 uppercase letters.")
    if not (len(target.zip_code) == ZIP_CODE_LEN and target.zip_code.isdigit()):
        raise ValueError("Zip code must include 5 digits.")


# Use this when a Person model is queried
# @listens_for(Person, "before_update")

# @listens_for(Member, "before_update")
# @listens_for(Provider, "before_update")
# def validate_person_update(_mapper, _connection, target):

