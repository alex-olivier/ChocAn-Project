# import os
# from sqlalchemy import create_engine 
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.sql import func
from models import (
    models, Base, Member, Provider, Service, ProviderService, ServiceRecord
)
from interactive_mode import InteractiveMode, interactive_mode
# from database_manager import DatabaseManager, get_session

from input_validation import prompt_until_valid


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
            interactive_mode = InteractiveMode()
            interactive_mode.main_menu()
        elif choice == "2":
            provider_terminal()
        elif choice == "3":
            manager_terminal()
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
