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
        self.member_manager = MemberManager(self.db_manager)
        self.provider_manager = ProviderManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)

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
    
    def menu(self):
        print("\n--- Interactive Mode ---")
        print(" [1] Add Member")
        print(" [2] Update Member")
        print(" [3] Delete Member")
        print(" [4] Add Provider")
        print(" [5] Update Provider")
        print(" [6] Delete Provider")
        print(" [7] Add Service")
        print(" [8] Update Service")
        print(" [9] Delete Service")
        print("[10] View Weekly Reports")
        print("[11] Exit")

        """
        Menu Design Example #1:
        ---------------------------------------------------
        Main Menu
        ---------------------------------------------------
        Main Menu:
          1. Interactive Mode
          2. Provider Terminal
          3. Manager Terminal
          4. Exit

        Enter your choice: 1

        ---------------------------------------------------
        Main Menu > Interactive Mode
        ---------------------------------------------------
        Main Menu:
          Interactive Mode:
            1. Member Management
            2. Provider Management
            3. Service Management
            4. View Weekly Reports
            5. Exit
        
        Enter your choice: 2

        ---------------------------------------------------
        Main Menu > Interactive Mode > Provider Management
        ---------------------------------------------------
        Main Menu:
          Interactive Mode:
            Provider Management:
              1. Add Provider
              2. Update Provider
              3. Delete Provider
              4. View Providers
              5. Exit
    
        Enter your choice: 5

        Menu Design Example #2:
        ---------------------------------------------------
        Main Menu
        ---------------------------------------------------
        Main Menu:
          1. Interactive Mode
          2. Provider Terminal
          3. Manager Terminal
          4. Exit

        Enter your choice: 3

        ---------------------------------------------------
        Main Menu > Manager Terminal
        ---------------------------------------------------
        Main Menu:
          Manager Terminal:
            1. Generate Weekly Reports
            2. Generate EFT Data
            3. Generate Provider Directory
            4. Exit
        
        Enter your choice: 1

        ---------------------------------------------------
        Main Menu > Interactive Mode > Provider Management
        ---------------------------------------------------
        Main Menu:
          Manager Terminal:
            Generate Weekly Reports:
              1. Generate Memeber Reports
              2. Update Provider
              3. Delete Provider
              4. View Providers
              5. Exit
    
        Enter your choice: 5

        
        """


        """
        # Interactive Mode using a Multi-Level Menu
        print("\n--- Interactive Mode ---")
        print("1. Member Management")
        print("  1. Add Member")
        print("  2. Update Member")
        print("  3. Delete Member")

        print("2. Provider Management")
        print("  1. Add Provider")
        print("  2. Update Provider")
        print("  3. Delete Provider")

        print("3. Service Management")
        print("  1. Add Service")
        print("  2. Update Service")
        print("  3. Delete Service")
        
        print("4. View Weekly Reports")
        print("5. Exit")
        """
        
        choice = input(">> ")
        if choice == '1':  # Add a member
            name, street_address, city, state, zip_code = self.prompt_person_details()
            self.member_manager.add_member(name, street_address, city, state, zip_code)
        
        elif choice == '2':  # Update a member
            member_id = self.prompt_until_valid(
                r'^\d{9}$',
                "Enter member ID to update: ",
                "Member ID must be 9 digits."
            )
            # TODO: Implement ability for user to update specific fields
            kwargs = {}
            self.member_manager.update_member(member_id, kwargs)
            print("Member updated.")
        
        elif choice == '3':  # Delete a member
            member_id = self.prompt_until_valid(
                r'^\d{9}$',
                "Enter member ID to delete: ",
                "Member ID must be 9 digits."
            )
            self.member_manager.delete_member(member_id)
            print("Member deleted.")
        
        elif choice == '4':  # Add a provider
            name, street_address, city, state, zip_code = self.prompt_person_details()
            self.person_manager.add_person(Provider, name, street_address, city, state, zip_code)
            print("Provider added.")
        
        elif choice == '5':  # Update a provider
            provider_id = input("Enter provider ID to update: ")
            name = input("Enter new provider name: ")
            number = input("Enter new provider number: ")
            address = input("Enter new address: ")
            city = input("Enter new city: ")
            state = input("Enter new state: ")
            zip_code = input("Enter new zip code: ")
            system.update_provider(provider_id, name, number, address, city, state, zip_code)
            print("Provider updated.")
        
        elif choice == '6':  # Delete a provider
            provider_id = input("Enter provider ID to delete: ")
            system.delete_provider(provider_id)
            print("Provider deleted.")
        
        elif choice == '7':  # Add a service
            service_code = input("Enter service code: ")
            service_name = input("Enter service name: ")
            fee = float(input("Enter service fee: "))
            system.add_service(service_code, service_name, fee)
            print("Service added.")
        
        elif choice == '8':  # View weekly reports
            system.generate_weekly_reports()
        
        elif choice == '9':
            print("Exiting manager menu.")
            return

"""
from person_manager import MemberManager, ProviderManager
from service_manager import ServiceManager
from record_manager import RecordManager
"""