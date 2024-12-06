from database_manager import DatabaseManager
from input_validation import prompt_until_valid
from constants import DATABASE_URL


class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url or DATABASE_URL)

    def run(self):
            print("\n")
            print("---------------------------------------------------")
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
            if choice == "1":  # TODO: Validate Member
                pass
            elif choice == "2":  # TODO: Record Service
                pass
            elif choice == "3":  # TODO: View Provider Directory
                pass
            elif choice == "4":
                print("Exiting... Goodbye!")
            else:
                print("Error occurred. Exiting...")

