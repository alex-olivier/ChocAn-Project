from database_manager import DatabaseManager
from person_manager import MemberManager, ProviderManager
from record_manager import RecordManager
from input_validation import prompt_until_valid
from constants import DATABASE_URL


class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)

    def main_menu(self, provider_number):
            print("\n---------------------------------------------------")
            print("Provider Terminal")
            print("---------------------------------------------------")
            print("Provider Terminal:")
            print("  1. Validate Member")
            print("  2. Record Service")
            print("  3. View Provider Directory")
            print("  4. Exit")

            choice = prompt_until_valid(
                r'^[1-4]$',
                "\nEnter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":
                member_number = prompt_until_valid(
                    r'^\d{9}$',
                    "Enter member number to delete: ",
                    "Member number must be 9 digits."
                )
                MemberManager(self.db_manager).is_valid_member(member_number)
            elif choice == "2":
                member_number = prompt_until_valid(
                    r'^\d{9}$',
                    "Enter member number: ",
                    "Member number must be 9 digits."
                )
                MemberManager(self.db_manager).is_valid_member(member_number)
                service_code = prompt_until_valid(
                    r'^\d{6}$',
                    "Enter service code: ",
                    "Service code must be 6 digits."
                )
                date_of_service = prompt_until_valid(
                    r'^\d{2}-\d{2}-\d{4}$',
                    "Enter date of service (MM-DD-YYYY): ",
                    "Date must be in the format MM-DD-YYYY."
                )
                comments = input("Enter comments (optional): ")
                RecordManager(self.db_manager).record_service(
                    provider_number, 
                    member_number, 
                    service_code, 
                    date_of_service, 
                    comments
                )
            elif choice == "3":  # TODO: View Provider Directory
                pass
            elif choice == "4":
                print("Exiting... Goodbye!")
            else:
                print("Error occurred. Exiting...")

    def validate_provider(self):
        provider_number = prompt_until_valid(
            r'^\d{9}$',
            "Enter provider number: ",
            "Provider number must be 9 digits."
        )
        if ProviderManager(self.db_manager).is_valid_provider(provider_number):
            return provider_number
        else:
            print("Invalid provider number.")
            return None

    def run(self):
        provider_number = self.validate_provider()
        if provider_number:
            self.main_menu(provider_number)
        else:
            print("Exiting... Goodbye!")