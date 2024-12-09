import sys
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.person_manager import MemberManager
from chocan_software.data_managers.person_manager import ProviderManager
from chocan_software.data_managers.service_manager import ServiceManager
from chocan_software.data_managers.service_record_manager import ServiceRecordManager
from chocan_software.string_utils import prompt_until_valid
from chocan_software.constants import (
    DATABASE_URL, 
    ACCOUNT_NUM_LEN, 
    SERVICE_CODE_LEN
)

"""
ProviderTerminal class:
Order of Operations for the Providers Terminal with a Single-line Output:
(1) Provider Terminal is switchd on.

(2) Terminal waits for provider number.

(3) Provider enters their provider number and if...
      a. it exists, terminal is activated and continue to (4).
      b. it doesn't exist, output "Invalid Number" and return to (2).

(4) Terminal waits for provider to enter a member number.

(5) Provider enters member number and if...
      a. it exists, then continue to (6).
      b. it doesn't exist, output "Invalid Number", then return to (4).

(6) Terminal checks the members status and if...
      a. it's valid, output "Validated", then continue to (7).
      b. it's suspended, output "Member Suspended", then return to (4).

(7) Terminal waits for provider to enter member number.

(8) Provider enters member number and waits for terminal to return "Validated".

(9) Terminal waits for provider to enter the date of the service.

(10) Provider enters date of service in the format "MM-DD-YYYY" and if...
      a. it's a valid format, continue to (11).
      b. it's a invalid format, output "Invalid Date", then return to (9).

(11) Terminal waits for provider to enter service code.

(12) Provider enters service code and if...
      a. it's valid, display the name of the service, then continue to (13).
      b. it's invalid, output "Invalid Code", then return to (11).
  
(13) Provider verifies the name of the service and if... 
      a. it's correct, enters 'y/Y' continue to (14).
      b. it's incorrect, enters 'n/N' return to (11).

(14) Terminal waits for provider to enter optional comments.

(15) Provider enters optional comments or leaves it blank.

(16) Terminal waits for provider to hit enter.

(17) Terminal outputs "Service Record Added" and returns to (4).
"""


class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url if db_url is not None else DATABASE_URL)
        self.provider_manager = ProviderManager(self.db_manager)
        self.member_manager = MemberManager(self.db_manager)
        self.service_record_manager = ServiceRecordManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)

    def validate_provider(self):
        provider_number = prompt_until_valid(
            rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
            "Enter provider number",
            "Provider number must be 9 digits"
        )
        if self.provider_manager.is_valid_provider(provider_number):
            while True:
                self.main_menu(provider_number)
                break
        else:
            print("Invalid Number")
            return
    
    def validate_member(self):
        member_number = prompt_until_valid(
            rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
            ">> Enter member number to delete: ",
            "Member number must be 9 digits."
        )
        self.member_manager.is_valid_member(member_number)

    def main_menu(self, provider_number):
            # print("\nProvider Terminal:")
            # print("  1. Validate Member")
            # print("  2. Create Service Record")
            # print("  3. View Provider Directory")
            # print("  4. Exit")

            choice = prompt_until_valid(
                r'^[1-4]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":
                self.validate_member()
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
