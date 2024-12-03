from database_manager import DatabaseManager
from person_manager import PersonManager
from service_manager import ServiceManager
from models import Member, Provider, Service, ServiceRecord
import re
from constants import (
    NAME_MIN_LEN, NAME_MAX_LEN, 
    STREET_MIN_LEN, STREET_MAX_LEN, 
    CITY_MIN_LEN, CITY_MAX_LEN, 
    STATE_LEN, 
    ZIP_CODE_LEN,
    SERVICE_NAME_MAX_LEN
)

class interactive_mode:
    def __init__(self):
        self.system = DatabaseManager()
        self.person_manager = PersonManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)

    # Validate user input with retry on failure
    def prompt_until_valid(regex, prompt_message, error_message):
        while True:
            value = input(prompt_message)
            if re.match(regex, value):
                return value
            print(error_message)

    def prompt_person_details(self):
        name = self.prompt_until_valid(rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$', "Enter member name (max 25 chars): ", "Invalid name (must be up to 25 characters).")
        street_address = self.prompt_until_valid(rf'^.{{{STREET_MIN_LEN},{STREET_MAX_LEN}}}$', "Enter street address (max 25 chars): ", "Invalid address (must be up to 25 characters).")
        city = self.prompt_until_valid(rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$', "Enter city (max 14 chars): ", "Invalid city (must be up to 14 characters).")
        state = self.prompt_until_valid(rf'^[A-Z]{{{STATE_LEN}}}$', "Enter state (2 letters): ", "Invalid state (must be 2 uppercase letters).")
        zip_code = self.prompt_until_valid(rf'^\d{{{ZIP_CODE_LEN}}}$', "Enter zip code (5 digits): ", "Invalid zip code (must be 5 digits).")
        return name, street_address, city, state, zip_code

    def prompt_service_details(self):
        name = self.prompt_until_valid(rf'^.{{1,{SERVICE_NAME_MAX_LEN}}}$', "Enter service name (max 25 chars): ", "Invalid name (must be up to 25 characters).")
        fee = self.prompt_until_valid(rf'^\d+(\.\d{1,2})?$', "Enter service fee: ", f"Invalid fee (must be a number up to {SERVICE_FEE_MAX}).")
        return name, float(fee)
    
    def manager_menu(self, system):
        print("\n--- Interactive Mode ---")
        print("1. Add a member")
        print("2. Update a member")
        print("3. Delete a member")
        print("4. Add a provider")
        print("5. Update a provider")
        print("6. Delete a provider")
        print("7. Add a service")
        print("8. View weekly reports")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            name, address, city, state, zip_code = system.prompt_person_details()
            self.person_manager.add_person(Member, name, number, address, city, state, zip_code)
        elif choice == '2':
            name = input("Enter new member name: ")
            address = input("Enter new address: ")
            city = input("Enter new city: ")
            state = input("Enter new state: ")
            zip_code = input("Enter new zip code: ")
            system.update_member(member_id, name, number, address, city, state, zip_code)
            print("Member updated.")
        elif choice == '3':
            member_id = input("Enter member ID to delete: ")
            system.delete_member(member_id)
            print("Member deleted.")
        elif choice == '4':
            name = input("Enter provider name: ")
            number = input("Enter provider number: ")
            address = input("Enter address: ")
            city = input("Enter city: ")
            state = input("Enter state: ")
            zip_code = input("Enter zip code: ")
            system.add_provider(name, number, address, city, state, zip_code)
            print("Provider added.")
        elif choice == '5':
            provider_id = input("Enter provider ID to update: ")
            name = input("Enter new provider name: ")
            number = input("Enter new provider number: ")
            address = input("Enter new address: ")
            city = input("Enter new city: ")
            state = input("Enter new state: ")
            zip_code = input("Enter new zip code: ")
            system.update_provider(provider_id, name, number, address, city, state, zip_code)
            print("Provider updated.")
        elif choice == '6':
            provider_id = input("Enter provider ID to delete: ")
            system.delete_provider(provider_id)
            print("Provider deleted.")
        elif choice == '7':
            service_code = input("Enter service code: ")
            service_name = input("Enter service name: ")
            fee = float(input("Enter service fee: "))
            system.add_service(service_code, service_name, fee)
            print("Service added.")
        elif choice == '8':
            system.generate_weekly_reports()
        elif choice == '9':
            print("Exiting manager menu.")
            return