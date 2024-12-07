# Stores constants for the program
"""
This module defines constants used throughout the program.

Constants:
    DATABASE_URL (str): The default URL for the database connection.
    TYPE_MAX_LEN (int): Maximum length for the type of person.
    NUMBER_LEN (int): Length of the person's number.
    NAME_MIN_LEN (int): Minimum length for the person's name.
    NAME_MAX_LEN (int): Maximum length for the person's name.
    STREET_ADDRESS_MIN_LEN (int): Minimum length for the person's street address.
    STREET_ADDRESS_MAX_LEN (int): Maximum length for the person's street address.
    CITY_MIN_LEN (int): Minimum length for the person's city.
    CITY_MAX_LEN (int): Maximum length for the person's city.
    STATE_LEN (int): Length of the person's state abbreviation.
    ZIP_CODE_LEN (int): Length of the person's ZIP code.
    SERVICE_CODE_LEN (int): Length of the service code.
    SERVICE_NAME_MIN_LEN (int): Minimum length for the service name.
    SERVICE_NAME_MAX_LEN (int): Maximum length for the service name.
    SERVICE_FEE_MAX (float): Maximum fee for a service.
    SERVICERECORD_COMMENT_MAX_LEN (int): Maximum length for comments in the service record.
"""

DATABASE_URL = "sqlite:///chocan.db"

NUMBER_LEN = 9
NAME_MIN_LEN = 1
NAME_MAX_LEN = 25
STREET_ADDRESS_MIN_LEN = 1
STREET_ADDRESS_MAX_LEN = 25
CITY_MIN_LEN = 1
CITY_MAX_LEN = 14
STATE_LEN = 2
ZIP_CODE_LEN = 5

SERVICE_CODE_LEN = 6
SERVICE_NAME_MIN_LEN = 1
SERVICE_NAME_MAX_LEN = 20
SERVICE_FEE_MAX = 999.99

RECORD_COMMENT_MAX_LEN = 100

# TYPE_MAX_LEN = 8