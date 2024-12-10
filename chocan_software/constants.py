# This module defines constants used throughout the program.
"""
Database constants:
    DATABASE_URL (str): The default URL for the database connection.

Member/Provider constants:
    ACCOUNT_NUM_LEN (int): Length of an account number (id padded w/ zeroes).
    NAME_MIN_LEN (int): Minimum length of a person's name.
    NAME_MAX_LEN (int): Maximum length of a person's name.
    STREET_ADDRESS_MIN_LEN (int): Minimum length of a person's street address.
    STREET_ADDRESS_MAX_LEN (int): Maximum length of a person's street address.
    CITY_MIN_LEN (int): Minimum length of a person's city.
    CITY_MAX_LEN (int): Maximum length of a person's city.
    STATE_LEN (int): Length of a person's state abbreviation.
    ZIP_CODE_LEN (int): Length of a person's ZIP code.

Member constants
    MEMBER_STATUS_ACTIVE (bool): Status of an active member.
    MEMBER_STATUS_SUSPENDED (bool): Status of a suspended member.
    
Service constants:
    SERVICE_CODE_LEN (int): Length of a service code (id padded w/ zeroes).
    SERVICE_NAME_MIN_LEN (int): Minimum length of a service name.
    SERVICE_NAME_MAX_LEN (int): Maximum length of a service name.
    SERVICE_FEE_MAX (float): Maximum fee for a service.

Service Record constants:
    SERVICERECORD_COMMENT_MAX_LEN (int): Maximum length of service record comments.
    
"""

# Database constants
DATABASE_URL = "sqlite:///test_data.db"
# DATABASE_URL = "sqlite:///chocan.db"

# Member/Provider constants
ACCOUNT_NUM_LEN = 9
NAME_MIN_LEN = 1
NAME_MAX_LEN = 25
STREET_ADDRESS_MIN_LEN = 1
STREET_ADDRESS_MAX_LEN = 25
CITY_MIN_LEN = 1
CITY_MAX_LEN = 14
STATE_LEN = 2
ZIP_CODE_LEN = 5

# Member constants
MEMBER_STATUS_ACTIVE = True
MEMBER_STATUS_SUSPENDED = False

# Service constants
SERVICE_CODE_LEN = 6
SERVICE_NAME_MIN_LEN = 1
SERVICE_NAME_MAX_LEN = 20
SERVICE_FEE_MAX = 999.99

# ServiceRecord constants
SERVICERECORD_COMMENT_MAX_LEN = 100
