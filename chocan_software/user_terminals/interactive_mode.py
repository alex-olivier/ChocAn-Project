import sys
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.person_manager import MemberManager
from chocan_software.data_managers.person_manager import ProviderManager
from chocan_software.data_managers.service_manager import ServiceManager
from chocan_software.string_utils import prompt_until_valid
from chocan_software.constants import (
    NAME_MIN_LEN,
    NAME_MAX_LEN,
    STREET_ADDRESS_MIN_LEN,
    STREET_ADDRESS_MAX_LEN,
    CITY_MIN_LEN,
    CITY_MAX_LEN,
    STATE_LEN,
    ZIP_CODE_LEN,
    ACCOUNT_NUM_LEN,
    SERVICE_CODE_LEN,
    SERVICE_NAME_MIN_LEN,
    SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX,
    MEMBER_STATUS_ACTIVE,
    MEMBER_STATUS_SUSPENDED
)


class InteractiveMode:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager is not None else DatabaseManager()
        self.member_manager = MemberManager(self.db_manager)
        self.provider_manager = ProviderManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)

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
        while True:
            print("\nManager Terminal:")
            print("  Interactive Mode:")
            print("    1. Member Management")
            print("    2. Provider Management")
            print("    3. Service Management")
            print("    4. Go Back")
            print("    5. Exit\n")
            choice = prompt_until_valid(
                r'^[1-5]$',
                ">> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Member Management
                self.member_management_menu()
            elif choice == "2": # Provider Management
                self.provider_management_menu()
            elif choice == "3": # Service Management
                self.service_management_menu()
            elif choice == "4": # Go Back
                return
            elif choice == "5": # Exit
                print("\nExiting... Goodbye!")
                sys.exit(0)
            else: # Catch all
                print("\nError occurred. Exiting...")
                sys.exit(1)

    def member_management_menu(self):
        while True:
            print("\nManager Terminal:")
            print("  Interactive Mode:")
            print("    Member Management:")
            print("      1. Add Member")
            print("      2. Update Member")
            print("      3. Delete Member")
            print("      4. View Members")
            print("      5. Go Back")
            print("      6. Exit\n")
            choice = prompt_until_valid(
                r'^[1-6]$',
                ">> Enter a choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Add a member
                print("\nEnter member details")
                name, street_address, city, state, zip_code = self.prompt_person_details()
                self.member_manager.add_member(
                    name, 
                    street_address, 
                    city, 
                    state, 
                    zip_code
                )
            elif choice == "2": # Update a member
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter member number to update: ",
                    "Member number must be 9 digits."
                )
                print("\nSelect the member field to update:")
                print("  1. Name")
                print("  2. Street Address")
                print("  3. City")
                print("  4. State")
                print("  5. ZIP Code")
                print("  6. Membership Status")
                print("  7. Cancel Update\n")
                field_choice = prompt_until_valid(
                    r'^[1-7]$',
                    ">> Enter your choice: ",
                    "Invalid choice. Please try again."
                )
                if field_choice == "1": # Update member name
                    new_name = prompt_until_valid(
                        rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
                        ">> New Name: ",
                        f"Name must be up to {NAME_MAX_LEN} characters."
                    )
                    kwargs = {"name": new_name}
                elif field_choice == "2": # Update member street address
                    new_street_address = prompt_until_valid(
                        rf'^.{{{STREET_ADDRESS_MIN_LEN},{STREET_ADDRESS_MAX_LEN}}}$',
                        ">> New Address: ",
                        f"  Street Address must be up to {STREET_ADDRESS_MAX_LEN} characters."
                    )
                    kwargs = {"street_address": new_street_address}
                elif field_choice == "3": # Update member city
                    new_city = prompt_until_valid(
                        rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
                        ">> New City: ",
                        f"  City must be up to {CITY_MAX_LEN} characters."
                    )
                    kwargs = {"city": new_city}
                elif field_choice == "4": # Update member state
                    new_state = prompt_until_valid(
                        rf'^[A-Z]{{{STATE_LEN}}}$',
                        ">> New State: ",
                        f"  State must include {STATE_LEN} uppercase letters."
                    )
                    kwargs = {"state": new_state}
                elif field_choice == "5": # Update member ZIP code
                    new_zip_code = prompt_until_valid(
                        rf'^\d{{{ZIP_CODE_LEN}}}$',
                        ">> New ZIP Code: ",
                        f"  ZIP Code must include {ZIP_CODE_LEN} digits."
                    )
                    kwargs = {"zip_code": new_zip_code}
                elif field_choice == "6": # Update member status
                    print("\nSelect the new member status:")
                    print("  1. Active")
                    print("  2. Suspended")
                    print("  3. Cancel Update\n")
                    status_choice = prompt_until_valid(
                        r'^[1-3]$',
                        ">> Enter your choice: ",
                        "Invalid choice. Please try again."
                    )
                    if status_choice == "1":
                        new_status = MEMBER_STATUS_ACTIVE
                    elif status_choice == "2" :
                        new_status = MEMBER_STATUS_SUSPENDED
                    elif status_choice == "3":
                        continue
                    kwargs = {"status": int(new_status)}
                elif field_choice == "7": # Cancel Update
                    continue
                self.member_manager.update_member(member_number, **kwargs)
            elif choice == "3": # Delete a member
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter member number to delete: ",
                    "Member number must be 9 digits."
                )
                self.member_manager.delete_member(member_number)
            elif choice == "4": # View Members
                print("\nMembers:")
                self.member_manager.view_members()
            elif choice == "5": # Go Back to previous menu
                return
            elif choice == "6": # Exit
                print("\nExiting... Goodbye!")
                sys.exit(0)
            else: # Catch all
                print("\nError occurred. Exiting...")
                sys.exit(1)

    def provider_management_menu(self):
        while True:
            print("\nManager Terminal:")
            print("  Interactive Mode:")
            print("    Provider Management:")
            print("      1. Add Provider")
            print("      2. Update Provider")
            print("      3. Delete Provider")
            print("      4. Add Provider Service")
            print("      5. View Provider Services")
            print("      6. View Providers")
            print("      7. Go Back")
            print("      8. Exit\n")
            choice = prompt_until_valid(
                r'^[1-8]$',
                ">> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Add a provider
                print("\nEnter provider details")
                name, street_address, city, state, zip_code = self.prompt_person_details()
                self.provider_manager.add_provider(name, street_address, city, state, zip_code)
            elif choice == "2": # Update a provider
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter provider number to update: ",
                    "Provider number must be 9 digits."
                )
                print("\nSelect the provider field to update:")
                print("  1. Name")
                print("  2. Street Address")
                print("  3. City")
                print("  4. State")
                print("  5. ZIP Code")
                print("  6. Cancel Update\n")
                field_choice = prompt_until_valid(
                    r'^[1-6]$',
                    ">> Enter your choice: ",
                    "Invalid choice. Please try again."
                )
                if field_choice == "1": # Update provider name
                    new_name = prompt_until_valid(
                        rf'^.{{{NAME_MIN_LEN},{NAME_MAX_LEN}}}$',
                        ">> New Name: ",
                        f"Name must be up to {NAME_MAX_LEN} characters."
                    )
                    kwargs = {"name": new_name}
                elif field_choice == "2": # Update provider street address
                    new_street_address = prompt_until_valid(
                        rf'^.{{{STREET_ADDRESS_MIN_LEN},{STREET_ADDRESS_MAX_LEN}}}$',
                        ">> New Street Address: ",
                        f"  Street Address must be up to {STREET_ADDRESS_MAX_LEN} characters."
                    )
                    kwargs = {"street_address": new_street_address}
                elif field_choice == "3": # Update provider city
                    new_city = prompt_until_valid(
                        rf'^.{{{CITY_MIN_LEN},{CITY_MAX_LEN}}}$',
                        ">> New City: ",
                        f"  City must be up to {CITY_MAX_LEN} characters."
                    )
                    kwargs = {"city": new_city}
                elif field_choice == "4": # Update provider state
                    new_state = prompt_until_valid(
                        rf'^[A-Z]{{{STATE_LEN}}}$',
                        ">> New State: ",
                        f"  State must include {STATE_LEN} uppercase letters."
                    )
                    kwargs = {"state": new_state}
                elif field_choice == "5": # Update provider ZIP code
                    new_zip_code = prompt_until_valid(
                        rf'^\d{{{ZIP_CODE_LEN}}}$',
                        ">> New ZIP Code: ",
                        f"  ZIP Code must include {ZIP_CODE_LEN} digits."
                    )
                    kwargs = {"zip_code": new_zip_code}
                elif field_choice == "6": # Cancel Update
                    continue
                self.provider_manager.update_provider(provider_number, **kwargs)
            elif choice == "3": # Delete a provider
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter provider number to delete: ",
                    "Provider number must be 9 digits."
                )
                self.provider_manager.delete_provider(provider_number)
            elif choice == "4": # Add provider service
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter provider number to add service: ",
                    "Provider number must be 9 digits."
                )
                service_code = prompt_until_valid(
                    rf'^\d{{{SERVICE_CODE_LEN}}}$',
                    ">> Enter service code to add to provider: ",
                    "Service code must be 6 digits."
                )
                self.provider_manager.add_provider_service(provider_number, service_code)
            elif choice == "5": # View provider services
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter provider number to view services: ",
                    "Provider number must be 9 digits."
                )
                services = self.provider_manager.get_provider_services(provider_number)
                print("\nProvider Services:")
                for service in services:
                    print(f"  {service.id:06}  {service.name:<20}  $ {service.fee:>6.2f}")
            elif choice == "6": # View Providers
                print("\nProviders:")
                self.provider_manager.view_providers()
            elif choice == "7": # Go Back to previous menu
                return
            elif choice == "8": # Exit
                print("\nExiting... Goodbye!")
                sys.exit(0)
            else: # Catch all
                print("\nError occurred. Exiting...")
                sys.exit(1)

    def service_management_menu(self):
        while True:
            print("\nManager Terminal:")
            print("  Interactive Mode:")
            print("    Service Management:")
            print("      1. Add Service")
            print("      2. Update Service")
            print("      3. Delete Service")
            print("      4. View Services")
            print("      5. Go Back")
            print("      6. Exit\n")
            choice = prompt_until_valid(
                r'^[1-6]$',
                ">> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Add a service
                name, fee = self.prompt_service_details()
                self.service_manager.add_service(name, fee)
            elif choice == "2": # Update Service
                choice = prompt_until_valid(
                    rf'^\d{{{SERVICE_CODE_LEN}}}$',
                    ">> Enter service code to update: ",
                    "Service code must be 6 digits."
                )
                print("\nSelect the service field to update:")
                print("  1. Name")
                print("  2. Fee")
                print("  3. Cancel Update\n")  
                field_choice = prompt_until_valid(
                    r'^[1-3]$',
                    ">> Enter your choice: ",
                    "Invalid choice. Please try again."
                )
                if field_choice == "1": # Update Service Name
                    new_name = prompt_until_valid(
                        rf'^.{{{SERVICE_NAME_MIN_LEN},{SERVICE_NAME_MAX_LEN}}}$',
                        ">> New Service Name: ",
                        f"Service Name must be up to {SERVICE_NAME_MAX_LEN} characters)."
                    )
                    kwargs = {"name": new_name}
                elif field_choice == "2": # Update Service Fee
                    new_fee = prompt_until_valid(
                        r'^\d{1,3}(\.\d{1,2})?$'  # 0-999.99 (2 decimal places)
                        ">> New Service Fee: ",
                        f"Service Fee cannot exceed ${SERVICE_FEE_MAX})."
                    )
                    kwargs = {"fee": new_fee}
                elif field_choice == "3": # Cancel Update
                    continue
                self.service_manager.update_service(service_code)
            elif choice == "3": # Delete Service
                service_code = prompt_until_valid(
                    rf'^\d{{{SERVICE_CODE_LEN}}}$',
                    ">> Enter service code to delete: ",
                    "Service code must be 6 digits."
                )
                self.service_manager.delete_service(service_code)
            elif choice == "4": # View Services
                print("\nServices:")
                self.service_manager.view_services()
            elif choice == "5": # Go Back to previous menu
                return
            elif choice == "6": # Exit
                print("\nExiting... Goodbye!")
                sys.exit(0)
            else: # Catch all
                print("\nError occurred. Exiting...")
                sys.exit(1)

        