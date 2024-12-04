# import os
# from sqlalchemy import create_engine 
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.sql import func
from models import (models, Base, Member, Provider, Service, ProviderService, ServiceRecord)
from interactive_mode import InteractiveMode
# from database_manager import DatabaseManager, get_session


import re


# Example ussage
if __name__ == "__main__":

    print("\n---- ChocAn Data Processing System ----")
    print("[1] Interactive Mode")
    print("[2] Manager Terminal")
    print("[3] Provider Terminal")
    print("[4] Generate EFT Data")
    print("[5] Generate Provider Directory")
    interactive_mode = InteractiveMode()

    add_member("John Doe", "123456789", "123 Main St", "Anytown", "CA", "90210")
    add_provider("Dr. Smith", "987654321", "456 Elm St", "Othertown", "NY", "10001")
    add_service("598470", "Dietitian Session", 150.00)
    record_service("987654321", "123456789", "598470", "11-24-2024", "Initial consultation")

    # Example usage of additional functionalities
    generate_member_report("123456789")
    generate_provider_report("987654321")
    # generate_eft_data()
    generate_summary_report()
