from database_manager import DatabaseManager
from person_manager import MemberManager, ProviderManager
from service_manager import ServiceManager
from record_manager import RecordManager
from models import Member, Provider, Service, ServiceRecord
import re
from constants import (
    DATABASE_URL,
    NAME_MIN_LEN, NAME_MAX_LEN, 
    STREET_MIN_LEN, STREET_MAX_LEN, 
    CITY_MIN_LEN, CITY_MAX_LEN, 
    STATE_LEN, 
    ZIP_CODE_LEN,
    SERVICE_NAME_MIN_LEN, SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX
)

class InteractiveMode:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)


    # Validate user input with retry on failure
    def prompt_until_valid(regex, prompt_message, error_message) -> str:
        while True:
            value = input(prompt_message)
            if re.match(regex, value):
                return value
            print(error_message)


    # Prompt ChocAn manager/operator for the details of a new member or provider
    def prompt_person_details(self) -> tuple:
        name = self.prompt_until_valid(
            rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
            "Enter name: ",
            "Name must be up to 25 characters."
        )
        street_address = self.prompt_until_valid(
            rf'^.{{{STREET_MIN_LEN},{STREET_MAX_LEN}}}$',
            "Enter street address: ",
            "Street address must be up to 25 characters."
        )
        city = self.prompt_until_valid(
            rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
            "Enter city: ",
            "City must be up to 14 characters."
        )
        state = self.prompt_until_valid(
            rf'^[A-Z]{{{STATE_LEN}}}$',
            "Enter state: ",
            "State must include 2 uppercase letters."
        )
        zip_code = self.prompt_until_valid(
            rf'^\d{{{ZIP_CODE_LEN}}}$',
            "Enter zip code: ",
            "Zip code must include 5 digits."
        )
        return name, street_address, city, state, zip_code


    # Prompt ChocAn manager/operator for the details of a new service
    def prompt_service_details(self) -> tuple:
        name = self.prompt_until_valid(
            rf'^.{{{SERVICE_NAME_MIN_LEN},{SERVICE_NAME_MAX_LEN}}}$',
            "Enter service name: ",
            "Service name must be up to 25 characters)."
        )
        fee = self.prompt_until_valid(
            r'^\d{1,3}(\.\d{1,2})?$'  # 0-999.99 (2 decimal places)
            "Enter service fee: ",
            f"Service fee cannot exceed ${SERVICE_FEE_MAX})."
        )
        return name, float(fee)


    def main_menu(self):
        print("\n---------------------------------------------------")
        print("Main Menu > Interactive Mode")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Interactive Mode:")
        print("    1. Member Management")
        print("    2. Provider Management")
        print("    3. Service Management")
        print("    4. Exit")
        choice = self.prompt_until_valid(
            r'^[1-4]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            self.member_management()
        elif choice == "2": 
            self.provider_management()
        elif choice == "3":
            self.service_management()
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


    def member_management(self):
        member_manager = MemberManager(self.db_manager)
        print("\n---------------------------------------------------")
        print("Main Menu > Interactive Mode > Member Management")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Interactive Mode:")
        print("    Member Management:")
        print("      1. Add Member")
        print("      2. Update Member")
        print("      3. Delete Member")
        print("      4. View Members")
        print("      5. Exit")
        choice = self.prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a member
            name, street_address, city, state, zip_code = self.prompt_person_details()
            member_manager.add_member(name, street_address, city, state, zip_code)
        
        elif choice == "2":  # Update a member
            member_id = self.prompt_until_valid(
                r'^\d{9}$',
                "Enter member ID to update: ",
                "Member ID must be 9 digits."
            )
            # TODO: Implement ability for user to update specific fields
            kwargs = {}
            member_manager.update_member(member_id, kwargs)
            print("Member updated.")
        
        elif choice == "3":  # Delete a member
            member_id = self.prompt_until_valid(
                r'^\d{9}$',
                "Enter member ID to delete: ",
                "Member ID must be 9 digits."
            )
            member_manager.delete_member(member_id)
            print("Member deleted.")
        elif choice == "4":  # View Members
            member_manager.view_members()
            pass
        elif choice == "5":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


    def provider_management(self):
        provider_manager = ProviderManager(self.db_manager)
        print("\n---------------------------------------------------")
        print("Main Menu > Interactive Mode > Provider Management")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Interactive Mode:")
        print("    Provider Management:")
        print("      1. Add Provider")
        print("      2. Update Provider")
        print("      3. Delete Provider")
        print("      4. View Providers")
        print("      5. Exit")
        choice = self.prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a provider
            name, street_address, city, state, zip_code = self.prompt_person_details()
            provider_manager.add_provider(name, street_address, city, state, zip_code)
            print("Provider added.")
        elif choice == "2":  # Update a provider
            provider_id = input("Enter provider ID to update: ")
            name = input("Enter new provider name: ")
            number = input("Enter new provider number: ")
            address = input("Enter new address: ")
            city = input("Enter new city: ")
            state = input("Enter new state: ")
            zip_code = input("Enter new zip code: ")

            name, street_address, city, state, zip_code = self.prompt_person_details()
            provider_manager.update_provider(provider_id, name, number, address, city, state, zip_code)
            print("Provider updated.")
        elif choice == "3":  # Delete a provider
            provider_id = input("Enter provider ID to delete: ")
            provider_manager.delete_provider(provider_id)
            print("Provider deleted.")
        elif choice == "4":  # View Providers
            # provider_manager.view_providers()
            pass  
        elif choice == "5":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


    def service_management(self):
        service_manager = ServiceManager(self.db_manager)
        print("\n---------------------------------------------------")
        print("Main Menu > Interactive Mode > Service Management")
        print("---------------------------------------------------")
        print("Main Menu:")
        print("  Interactive Mode:")
        print("    Service Management:")
        print("      1. Add Service")
        print("      2. Update Service")
        print("      3. Delete Service")
        print("      4. View Services")
        print("      5. Exit")
        choice = self.prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a service
            service_name, fee = self.prompt_service_details()
            service_manager.add_service(service_name, fee)
            print("Service added.")
        elif choice == "2":  # Update Service
            # service_manager.update_service()
            pass
        elif choice == "3":  # Delete Service
            # service_manager.delete_service()
            pass
        elif choice == "4":  # View Services
            # service_manager.view_services()
            pass
        elif choice == "5":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")
        


"""
from person_manager import MemberManager, ProviderManager
from service_manager import ServiceManager
from record_manager import RecordManager
"""