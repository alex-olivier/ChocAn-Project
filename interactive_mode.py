from database_manager import DatabaseManager
from person_manager import MemberManager, ProviderManager
from service_manager import ServiceManager
from input_validation import prompt_until_valid
from constants import (
    DATABASE_URL,
    PERSON_NAME_MIN_LEN, PERSON_NAME_MAX_LEN, 
    PERSON_STREET_ADDRESS_MIN_LEN, PERSON_STREET_ADDRESS_MAX_LEN, 
    PERSON_CITY_MIN_LEN, PERSON_CITY_MAX_LEN, 
    PERSON_STATE_LEN, 
    PERSON_ZIP_CODE_LEN,
    SERVICE_NAME_MIN_LEN, SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX
)

class InteractiveMode:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)

    # Prompt ChocAn manager/operator for the details of a new member or provider
    def prompt_person_details(self) -> tuple:
        name = prompt_until_valid(
            rf'^.{{{PERSON_NAME_MIN_LEN},{PERSON_NAME_MAX_LEN}}}$',
            "Enter name: ",
            f"Name must be up to {PERSON_NAME_MAX_LEN} characters."
        )
        street_address = prompt_until_valid(
            rf'^.{{{PERSON_STREET_ADDRESS_MIN_LEN},{PERSON_STREET_ADDRESS_MAX_LEN}}}$',
            "Enter street address: ",
            f"Street address must be up to {PERSON_STREET_ADDRESS_MAX_LEN} characters."
        )
        city = prompt_until_valid(
            rf'^.{{{PERSON_CITY_MIN_LEN},{PERSON_CITY_MAX_LEN}}}$',
            "Enter city: ",
            f"City must be up to {PERSON_CITY_MAX_LEN} characters."
        )
        state = prompt_until_valid(
            rf'^[A-Z]{{{PERSON_STATE_LEN}}}$',
            "Enter state: ",
            f"State must include {PERSON_STATE_LEN} uppercase letters."
        )
        zip_code = prompt_until_valid(
            rf'^\d{{{PERSON_ZIP_CODE_LEN}}}$',
            "Enter zip code: ",
            f"Zip code must include {PERSON_ZIP_CODE_LEN} digits."
        )
        return name, street_address, city, state, zip_code


    # Prompt ChocAn manager/operator for the details of a new service
    def prompt_service_details(self) -> tuple:
        name = prompt_until_valid(
            rf'^.{{{SERVICE_NAME_MIN_LEN},{SERVICE_NAME_MAX_LEN}}}$',
            "Enter service name: ",
            f"Service name must be up to {SERVICE_NAME_MAX_LEN} characters)."
        )
        fee = prompt_until_valid(
            r'^\d{1,3}(\.\d{1,2})?$'  # 0-999.99 (2 decimal places)
            "Enter service fee: ",
            f"Service fee cannot exceed ${SERVICE_FEE_MAX})."
        )
        return name, float(fee)


    def run(self):
        print("\n---------------------------------------------------")
        print("Interactive Mode")
        print("---------------------------------------------------")
        print("Interactive Mode:")
        print("  1. Member Management")
        print("  2. Provider Management")
        print("  3. Service Management")
        print("  4. Exit")
        
        choice = prompt_until_valid(
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
        print("Interactive Mode > Member Management")
        print("---------------------------------------------------")
        print("Interactive Mode:")
        print("  Member Management:")
        print("    1. Add Member")
        print("    2. Update Member")
        print("    3. Delete Member")
        print("    4. View Members")
        print("    5. Exit")
        
        choice = prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a member
            name, street_address, city, state, zip_code = self.prompt_person_details()
            member_manager.add_member(name, street_address, city, state, zip_code)
        
        elif choice == "2": # Update a member
            # TODO: Implement ability for user to update specific fields
            member_id = prompt_until_valid(
                r'^\d{9}$',
                "Enter member number to update: ",
                "Member number must be 9 digits."
            )
            
            kwargs = {}
            member_manager.update_member(member_id, kwargs)
            print("Member updated.")
        
        elif choice == "3":  # Delete a member
            member_id = prompt_until_valid(
                r'^\d{9}$',
                "Enter member number to delete: ",
                "Member number must be 9 digits."
            )
            member_manager.delete_member(member_id)
            print("Member deleted.")
        elif choice == "4":  # View Members
            member_manager.view_members()
        elif choice == "5":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


    def provider_management(self):
        provider_manager = ProviderManager(self.db_manager)
        print("\n---------------------------------------------------")
        print("Interactive Mode > Provider Management")
        print("---------------------------------------------------")
        print("Interactive Mode:")
        print("  Provider Management:")
        print("    1. Add Provider")
        print("    2. Update Provider")
        print("    3. Delete Provider")
        print("    4. View Providers")
        print("    5. Exit")
        
        choice = prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a provider
            name, street_address, city, state, zip_code = self.prompt_person_details()
            provider_manager.add_provider(name, street_address, city, state, zip_code)
            print("Provider added.")
        elif choice == "2": # Update a provider
            # TODO: Implement ability to update specific fields
            provider_id = prompt_until_valid(
                r'^\d{9}$',
                "Enter provider number to update: ",
                "Provider number must be 9 digits."
            )
            kwargs = {}
            provider_manager.update_member(provider_id, kwargs)
            print("Provider updated.")
        elif choice == "3":  # Delete a provider
            provider_id = prompt_until_valid(
                r'^\d{9}$',
                "Enter provider number to delete: ",
                "Provider number must be 9 digits."
            )
            provider_manager.delete_provider(provider_id)
            print("Provider deleted.")
        elif choice == "4":  # View Providers
            provider_manager.view_providers()
        elif choice == "5":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")


    def service_management(self):
        service_manager = ServiceManager(self.db_manager)
        print("\n---------------------------------------------------")
        print("Interactive Mode > Service Management")
        print("---------------------------------------------------")
        print("Interactive Mode:")
        print("  Service Management:")
        print("    1. Add Service")
        print("    2. Update Service")
        print("    3. Delete Service")
        print("    4. View Services")
        print("    5. Exit")
        choice = prompt_until_valid(
            r'^[1-5]$',
            "\nEnter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a service
            service_name, fee = self.prompt_service_details()
            service_manager.add_service(service_name, fee)
            print("Service added.")
        elif choice == "2":  # Update Service
            choice = prompt_until_valid(
                r'^\d{6}$',
                "\nEnter service code to update: ",
                "Service code must be 6 digits."
            )
            service_manager.update_service(service_code)
            pass
        elif choice == "3":  # Delete Service
            service_code = prompt_until_valid(
                r'^\d{6}$',
                "\nEnter service code to delete: ",
                "Service code must be 6 digits."
            )
            service_manager.delete_service(service_code)
            pass
        elif choice == "4":  # View Services
            service_manager.view_services()
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