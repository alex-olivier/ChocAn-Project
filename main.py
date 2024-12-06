# import os
# from sqlalchemy import create_engine 
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.sql import func
from models import (
    models, Base, Member, Provider, Service, ProviderService, ServiceRecord
)
from interactive_mode import InteractiveMode
# from database_manager import DatabaseManager, get_session

import re


# Validate user input with retry on failure
def prompt_until_valid(regex, prompt_message, error_message) -> str:
    while True:
        value = input(prompt_message)
        if re.match(regex, value):
            return value
        print(error_message)

# TODO: Fix main_menu() to call the correct functions
def main_menu():
        print("\n---------------------------------------------------")
        print("Main Menu")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  1. Interactive Mode")
        print("  2. Provider Terminal")
        print("  3. Manager Terminal")
        print("  4. Exit")
        choice = prompt_until_valid(
            r'^[1-4]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            interactive_mode()
        elif choice == "2":
            provider_terminal()
        elif choice == "3":
            manager_terminal()
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


# TODO: Fix interactive_mode() to call the correct functions
# def interactive_mode():
#         print("\n---------------------------------------------------")
#         print("Main Menu > Interactive Mode")
#         print("---------------------------------------------------")
#         print("Main Menu:")
#         print("  Interactive Mode:")
#         print("    1. Member Management")
#         print("    2. Provider Management")
#         print("    3. Service Management")
#         print("    4. Exit")
#         choice = prompt_until_valid(
#             r'^[1-4]$',
#             "\nEnter your choice: ",
#             "Invalid choice. Please try again."
#         )
#         if choice == "1":
#             member_management()
#         elif choice == "2":
#             provider_management()
#         elif choice == "3":
#             service_management()
#         elif choice == "4":
#             print("Exiting... Goodbye!")
#         else:
#             print("Error occurred. Exiting...")

# TODO: Fix member_management() to call the correct functions
# def member_management():
#         print("\n---------------------------------------------------")
#         print("Main Menu > Interactive Mode > Member Management")
#         print("---------------------------------------------------")
#         print("Main Menu:")
#         print("  Interactive Mode:")
#         print("    Member Management:")
#         print("      1. Add Member")
#         print("      2. Update Member")
#         print("      3. Delete Member")
#         print("      4. View Members")
#         print("      5. Exit")
#         choice = prompt_until_valid(
#             r'^[1-5]$',
#             "\nEnter your choice: ",
#             "Invalid choice. Please try again."
#         )
#         if choice == "1":
#             pass  # Add Member
#         elif choice == "2":
#             pass  # Update Member
#         elif choice == "3":
#             pass  # Delete Member
#         elif choice == "4":
#             pass  # View Members
#         elif choice == "5":
#             print("Exiting... Goodbye!")
#         else:
#             print("Error occurred. Exiting...")

# TODO: Fix provider_management() to call the correct functions
# def provider_management():
#         print("\n---------------------------------------------------")
#         print("Main Menu > Interactive Mode > Provider Management")
#         print("---------------------------------------------------")
#         print("Main Menu:")
#         print("  Interactive Mode:")
#         print("    Provider Management:")
#         print("      1. Add Provider")
#         print("      2. Update Provider")
#         print("      3. Delete Provider")
#         print("      4. View Providers")
#         print("      5. Exit")
#         choice = prompt_until_valid(
#             r'^[1-5]$',
#             "\nEnter your choice: ",
#             "Invalid choice. Please try again."
#         )
#         if choice == "1":
#             pass  # Add Provider
#         elif choice == "2":
#             pass  # Update Provider
#         elif choice == "3":
#             pass  # Delete Provider
#         elif choice == "4":
#             pass  # View Providers
#         elif choice == "5":
#             print("Exiting... Goodbye!")
#         else:
#             print("Error occurred. Exiting...")

# TODO: Fix service_management() to call the correct functions
# def service_management():
#         print("\n---------------------------------------------------")
#         print("Main Menu > Interactive Mode > Service Management")
#         print("---------------------------------------------------")
#         print("Main Menu:")
#         print("  Interactive Mode:")
#         print("    Service Management:")
#         print("      1. Add Service")
#         print("      2. Update Service")
#         print("      3. Delete Service")
#         print("      4. View Services")
#         print("      5. Exit")
#         choice = prompt_until_valid(
#             r'^[1-5]$',
#             "\nEnter your choice: ",
#             "Invalid choice. Please try again."
#         )
#         if choice == "1":
#             pass  # Add Service
#         elif choice == "2":
#             pass  # Update Service
#         elif choice == "3":
#             pass  # Delete Service
#         elif choice == "4":
#             pass  # View Services
#         elif choice == "5":
#             print("Exiting... Goodbye!")
#         else:
#             print("Error occurred. Exiting...")

# TODO: Fix provider_terminal() to call the correct functions
def provider_terminal():
        print("\n---------------------------------------------------")
        print("Main Menu > Provider Terminal")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Provider Terminal:")
        print("    1. Validate Member")
        print("    2. Record Service")
        print("    3. View Provider Directory")
        print("    4. Exit")
        choice = prompt_until_valid(
            r'^[1-4]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            pass  # Validate Member
        elif choice == "2":
            pass  # Record Service
        elif choice == "3":
            pass  # View Provider Directory
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")

# TODO: Fix manager_terminal() to call the correct functions
def manager_terminal():
        print("\n---------------------------------------------------")
        print("Main Menu > Manager Terminal")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Manager Terminal:")
        print("    1. Report Management")
        print("    2. Generate EFT Data")
        print("    3. Generate Provider Directory")
        print("    4. Exit")
        choice = prompt_until_valid(
            r'^[1-4]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            pass  # Report Management
        elif choice == "2":
            pass  # Generate EFT Data
        elif choice == "3":
            pass  # Generate Provider Directory
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")

# TODO: Fix report_management() to call the correct functions
def report_management():
        print("\n---------------------------------------------------")
        print("Main Menu > Manager Terminal > Report Management")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Manager Terminal:")
        print("    Report Management:")
        print("      1. Main Accounting Procedure")
        print("      2. Generate Member Report")
        print("      3. Generate Provider Report")
        print("      4. Exit")
        choice = prompt_until_valid(
            r'^[1-4]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            pass  # Main Accounting Procedure
        elif choice == "2":
            pass  # Generate Member Report
        elif choice == "3":
            pass  # Generate Provider Report
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")

# TODO: Fix main() to call the correct functions
if __name__ == "__main__":
    main_menu()



# # Example ussage
# if __name__ == "__main__":

#     print("\n---- ChocAn Data Processing System ----")
#     print("[1] Interactive Mode")
#     print("[2] Manager Terminal")
#     print("[3] Provider Terminal")
#     print("[4] Generate EFT Data")
#     print("[5] Generate Provider Directory")
#     interactive_mode = InteractiveMode()

#     add_member("John Doe", "123456789", "123 Main St", "Anytown", "CA", "90210")
#     add_provider("Dr. Smith", "987654321", "456 Elm St", "Othertown", "NY", "10001")
#     add_service("598470", "Dietitian Session", 150.00)
#     record_service("987654321", "123456789", "598470", "11-24-2024", "Initial consultation")

#     # Example usage of additional functionalities
#     generate_member_report("123456789")
#     generate_provider_report("987654321")
#     # generate_eft_data()
#     generate_summary_report()
