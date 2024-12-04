# Stores constants for the program
"""
This module defines constants used throughout the program.

Constants:
    DATABASE_URL (str): The default URL for the database connection.
    PERSON_TYPE_MAX_LEN (int): Maximum length for the type of person.
    PERSON_NUMBER_LEN (int): Length of the person's number.
    PERSON_NAME_MIN_LEN (int): Minimum length for the person's name.
    PERSON_NAME_MAX_LEN (int): Maximum length for the person's name.
    PERSON_STREET_ADDRESS_MIN_LEN (int): Minimum length for the person's street address.
    PERSON_STREET_ADDRESS_MAX_LEN (int): Maximum length for the person's street address.
    PERSON_CITY_MIN_LEN (int): Minimum length for the person's city.
    PERSON_CITY_MAX_LEN (int): Maximum length for the person's city.
    PERSON_STATE_LEN (int): Length of the person's state abbreviation.
    PERSON_ZIP_CODE_LEN (int): Length of the person's ZIP code.
    SERVICE_CODE_LEN (int): Length of the service code.
    SERVICE_NAME_MIN_LEN (int): Minimum length for the service name.
    SERVICE_NAME_MAX_LEN (int): Maximum length for the service name.
    SERVICE_FEE_MAX (float): Maximum fee for a service.
    SERVICERECORD_COMMENT_MAX_LEN (int): Maximum length for comments in the service record.
"""

DATABASE_URL = "sqlite:///chocan.db"

PERSON_TYPE_MAX_LEN = 8
PERSON_NUMBER_LEN = 9
PERSON_NAME_MIN_LEN = 1
PERSON_NAME_MAX_LEN = 25
PERSON_STREET_ADDRESS_MIN_LEN = 1
PERSON_STREET_ADDRESS_MAX_LEN = 25
PERSON_CITY_MIN_LEN = 1
PERSON_CITY_MAX_LEN = 14
PERSON_STATE_LEN = 2
PERSON_ZIP_CODE_LEN = 5

SERVICE_CODE_LEN = 6
SERVICE_NAME_MIN_LEN = 1
SERVICE_NAME_MAX_LEN = 20
SERVICE_FEE_MAX = 999.99

SERVICERECORD_COMMENT_MAX_LEN = 100
