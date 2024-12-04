import os
# import models
from models import (models, Base, Member, Provider, Service, ProviderService, ServiceRecord)
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

import re


# ChocAn Database Operations







################################################################################
# ADDITIONAL FUNCTIONALITY
################################################################################




# Example usage
if __name__ == "__main__":
    add_member("John Doe", "123456789", "123 Main St", "Anytown", "CA", "90210")
    add_provider("Dr. Smith", "987654321", "456 Elm St", "Othertown", "NY", "10001")
    add_service("598470", "Dietitian Session", 150.00)
    record_service("987654321", "123456789", "598470", "11-24-2024", "Initial consultation")

    # Example usage of additional functionalities
    generate_member_report("123456789")
    generate_provider_report("987654321")
    # generate_eft_data()
    generate_summary_report()
