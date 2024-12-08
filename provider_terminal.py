import sys
from database_manager import DatabaseManager
from person_manager import MemberManager, ProviderManager
from service_record_manager import ServiceRecordManager
from service_manager import ServiceManager
from string_utils import prompt_until_valid
from constants import (
    DATABASE_URL, ACCOUNT_NUM_LEN, SERVICE_CODE_LEN
)


class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)
        self.provider_manager = ProviderManager(self.db_manager)
        self.person_manager = MemberManager(self.db_manager)
        self.service_record_manager = ServiceRecordManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)

    def main_menu(self, provider_number):
            print("\nProvider Terminal:")
            print("  1. Validate Member")
            print("  2. Create Service Record")
            print("  3. View Provider Directory")
            print("  4. Exit")

            choice = prompt_until_valid(
                r'^[1-4]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter member number to delete: ",
                    "Member number must be 9 digits."
                )
                self.member_manager.is_valid_member(member_number)
            elif choice == "2":
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter member number: ",
                    "Member number must be 9 digits."
                )
                self.member_manager.is_valid_member(member_number)
                service_code = prompt_until_valid(
                    rf'^\d{{{SERVICE_CODE_LEN}}}$',
                    ">> Enter service code: ",
                    "Service code must be 6 digits."
                )
                date_of_service = prompt_until_valid(
                    r'^\d{2}-\d{2}-\d{4}$',  # MM-DD-YYYY
                    ">> Enter date of service (MM-DD-YYYY): ",
                    "Date must be in the format MM-DD-YYYY."
                )
                comments = input(">> Enter comments (optional): ")
                self.service_record_manager.add_service_record(
                    provider_number, 
                    member_number, 
                    service_code, 
                    date_of_service, 
                    comments
                )
            elif choice == "3":
                ServiceManager(self.db_manager).view_services()
            elif choice == "4":
                print("Exiting... Goodbye!")
                return
            else:  # catch all
                print("Error occurred. Exiting...")
                sys.exit(1)

    def run(self):
        provider_number = prompt_until_valid(
            rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
            ">> Enter provider number: ",
            "Provider number must be 9 digits."
        )
        if self.provider_manager.is_valid_provider(provider_number):
            while True:
                self.main_menu(provider_number)
                break
        else:
            print("Invalid provider number.")
            return