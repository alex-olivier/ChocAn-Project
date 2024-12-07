import sys
from database_manager import DatabaseManager
from person_manager import MemberManager, ProviderManager
from service_manager import ServiceManager
from string_utils import prompt_until_valid
from constants import (
    DATABASE_URL, NAME_MIN_LEN, NAME_MAX_LEN, STREET_ADDRESS_MIN_LEN,
    STREET_ADDRESS_MAX_LEN, CITY_MIN_LEN, CITY_MAX_LEN, STATE_LEN, ZIP_CODE_LEN,
    ACCOUNT_NUM_LEN, SERVICE_CODE_LEN, SERVICE_NAME_MIN_LEN, SERVICE_NAME_MAX_LEN, SERVICE_FEE_MAX
)


class InteractiveMode:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)

    # Prompt ChocAn manager/operator for the details of a new member or provider
    def prompt_person_details(self) -> tuple:
        name = prompt_until_valid(
            rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
            ">> Name: ",
            f"Name must be up to {NAME_MAX_LEN} characters."
        )
        street_address = prompt_until_valid(
            rf'^.{{{STREET_ADDRESS_MIN_LEN},{STREET_ADDRESS_MAX_LEN}}}$',
            ">> Street Address: ",
            f"Street Address must be up to {STREET_ADDRESS_MAX_LEN} characters."
        )
        city = prompt_until_valid(
            rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
            ">> City: ",
            f"City must be up to {CITY_MAX_LEN} characters."
        )
        state = prompt_until_valid(
            rf'^[A-Z]{{{STATE_LEN}}}$',
            ">> State: ",
            f"State must include {STATE_LEN} uppercase letters."
        )
        zip_code = prompt_until_valid(
            rf'^\d{{{ZIP_CODE_LEN}}}$',
            ">> ZIP Code: ",
            f"ZIP Code must include {ZIP_CODE_LEN} digits."
        )
        return name, street_address, city, state, zip_code

    # Prompt ChocAn manager/operator for the details of a new service
    def prompt_service_details(self) -> tuple:
        name = prompt_until_valid(
            rf'^.{{{SERVICE_NAME_MIN_LEN},{SERVICE_NAME_MAX_LEN}}}$',
            ">> Service Name: ",
            f"Service Name must be up to {SERVICE_NAME_MAX_LEN} characters)."
        )
        fee = prompt_until_valid(
            r'^\d{1,3}(\.\d{1,2})?$',  # 0-999.99 (2 decimal places)
            ">> Service Fee: ",
            f"Service Fee cannot exceed ${SERVICE_FEE_MAX})."
        )
        return name, float(fee)

    def main_menu(self):
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
            "\n>> Enter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":
            self.member_management()
        elif choice == "2": 
            self.provider_management()
        elif choice == "3":
            self.service_management()
        elif choice == "4":
            print("\nExiting... Goodbye!")
            # return
            sys.exit()
        else: # Catch all
            print("\nError occurred. Exiting...")
            sys.exit()

    def member_management(self):
        member_manager = MemberManager(self.db_manager)
        while True:
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
                "\n>> Enter a choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":  # Add a member
                print("\nEnter member details")
                name, street_address, city, state, zip_code = self.prompt_person_details()
                member_manager.add_member(name, street_address, city, state, zip_code)
            elif choice == "2": # Update a member
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    "\n>> Enter member number to update: ",
                    "Member number must be 9 digits."
                )

                print("\nSelect the member field to update:")
                print("  1. Name")
                print("  2. Street Address")
                print("  3. City")
                print("  4. State")
                print("  5. ZIP Code")
                print("  6. Membership Status")
                field_choice = prompt_until_valid(
                    r'^[1-5]$',
                    "\n>> Enter your choice: ",
                    "Invalid choice. Please try again."
                )

                if field_choice == "1":
                    new_name = prompt_until_valid(
                        rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
                        ">> New Name: ",
                        f"Name must be up to {NAME_MAX_LEN} characters."
                    )
                    kwargs = {"name": new_name}
                elif field_choice == "2":
                    new_street_address = prompt_until_valid(
                        rf'^.{{{STREET_ADDRESS_MIN_LEN},{STREET_ADDRESS_MAX_LEN}}}$',
                        ">> Street Address: ",
                        f"  Street Address must be up to {STREET_ADDRESS_MAX_LEN} characters."
                    )
                    kwargs = {"street_address": new_street_address}
                elif field_choice == "3":
                    new_city = prompt_until_valid(
                        rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
                        ">> City: ",
                        f"  City must be up to {CITY_MAX_LEN} characters."
                    )
                    kwargs = {"city": new_city}
                elif field_choice == "4":
                    new_state = prompt_until_valid(
                        rf'^[A-Z]{{{STATE_LEN}}}$',
                        ">> State: ",
                        f"  State must include {STATE_LEN} uppercase letters."
                    )
                    kwargs = {"state": new_state}
                elif field_choice == "5":
                    new_zip_code = prompt_until_valid(
                        rf'^\d{{{ZIP_CODE_LEN}}}$',
                        ">> ZIP Code: ",
                        f"  ZIP Code must include {ZIP_CODE_LEN} digits."
                    )
                    kwargs = {"zip_code": new_zip_code}
                # elif field_choice == "6":
                    # print("")
                    # new_status = 
                    # kwargs = {"status": new_status}
                member_manager.update_member(member_number, **kwargs)
            elif choice == "3":  # Delete a member
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    "\n>> Enter member number to delete: ",
                    "Member number must be 9 digits."
                )
                member_manager.delete_member(member_number)
            elif choice == "4":  # View Members
                
                member_manager.view_members()
            elif choice == "5":
                print("\nExiting... Goodbye!")
                return
            else: # Catch all
                print("\nError occurred. Exiting...")
                sys.exit()

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
            "\n>> Enter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a provider
            print("\nEnter provider details")
            name, street_address, city, state, zip_code = self.prompt_person_details()
            provider_manager.add_provider(name, street_address, city, state, zip_code)
        elif choice == "2": # Update a provider
            provider_number = prompt_until_valid(
                rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                ">> Enter provider number to update: ",
                "Provider number must be 9 digits."
            )

             # Prompt the user to select the field to update
            print("\nSelect the provider field to update:")
            print("  1. Name")
            print("  2. Street Address")
            print("  3. City")
            print("  4. State")
            print("  5. ZIP Code")

            field_choice = prompt_until_valid(
                r'^[1-5]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if field_choice == "1":
                new_name = prompt_until_valid(
                    rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
                    ">> New Name: ",
                    f"Name must be up to {NAME_MAX_LEN} characters."
                )
                kwargs = {"name": new_name}
            elif field_choice == "2":
                new_street_address = prompt_until_valid(
                    rf'^.{{{STREET_ADDRESS_MIN_LEN},{STREET_ADDRESS_MAX_LEN}}}$',
                    ">> Street Address: ",
                    f"  Street Address must be up to {STREET_ADDRESS_MAX_LEN} characters."
                )
                kwargs = {"street_address": new_street_address}
            elif field_choice == "3":
                new_city = prompt_until_valid(
                    rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
                    ">> City: ",
                    f"  City must be up to {CITY_MAX_LEN} characters."
                )
                kwargs = {"city": new_city}
            elif field_choice == "4":
                new_state = prompt_until_valid(
                    rf'^[A-Z]{{{STATE_LEN}}}$',
                    ">> State: ",
                    f"  State must include {STATE_LEN} uppercase letters."
                )
                kwargs = {"state": new_state}
            elif field_choice == "5":
                new_zip_code = prompt_until_valid(
                    rf'^\d{{{ZIP_CODE_LEN}}}$',
                    ">> ZIP Code: ",
                    f"  ZIP Code must include {ZIP_CODE_LEN} digits."
                )
                kwargs = {"zip_code": new_zip_code}
            provider_manager.update_provider(provider_number, **kwargs)
        elif choice == "3":  # Delete a provider
            provider_number = prompt_until_valid(
                rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                "\nEnter provider number to delete: ",
                "Provider number must be 9 digits."
            )
            provider_manager.delete_provider(provider_number)
        elif choice == "4":  # View Providers
            provider_manager.view_providers()
        elif choice == "5":
            print("\nExiting... Goodbye!")
            return
        else: # Catch all
            print("\nError occurred. Exiting...")
            sys.exit()

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
            "\n>> Enter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Add a service
            name, fee = self.prompt_service_details()
            service_manager.add_service(name, fee)
        elif choice == "2":  # Update Service
            choice = prompt_until_valid(
                rf'^\d{{{SERVICE_CODE_LEN}}}$',
                ">> Enter service code to update: ",
                "Service code must be 6 digits."
            )

            # Prompt the user to select the field to update
            print("\nSelect the service field to update:")
            print("  1. Name")
            print("  2. Fee")
            
            field_choice = prompt_until_valid(
                r'^[1-2]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if field_choice == "1":
                new_name = prompt_until_valid(
                    rf'^.{{{SERVICE_NAME_MIN_LEN},{SERVICE_NAME_MAX_LEN}}}$',
                    ">> Service Name: ",
                    f"Service Name must be up to {SERVICE_NAME_MAX_LEN} characters)."
                )
                kwargs = {"name": new_name}
            elif field_choice == "2":
                new_fee = prompt_until_valid(
                    r'^\d{1,3}(\.\d{1,2})?$'  # 0-999.99 (2 decimal places)
                    ">> Service Fee: ",
                    f"Service Fee cannot exceed ${SERVICE_FEE_MAX})."
                )
                kwargs = {"fee": new_fee}

            service_manager.update_service(service_code)
        elif choice == "3":  # Delete Service
            service_code = prompt_until_valid(
                rf'^\d{{{SERVICE_CODE_LEN}}}$',
                "\n>> Enter service code to delete: ",
                "Service code must be 6 digits."
            )
            service_manager.delete_service(service_code)
        elif choice == "4":  # View Services
            service_manager.view_services()
        elif choice == "5":
            print("\nExiting... Goodbye!")
            return
        else: # Catch all
            print("\nError occurred. Exiting...")
            sys.exit()

    def run(self):
        while True:
            self.main_menu()
        