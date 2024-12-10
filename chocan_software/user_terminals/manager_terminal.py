import sys
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.report_manager import ReportManager
from chocan_software.user_terminals.interactive_mode import InteractiveMode
from chocan_software.string_utils import prompt_until_valid
from chocan_software.constants import (
    DATABASE_URL, 
    ACCOUNT_NUM_LEN
)


class ManagerTerminal:
    def __init__(self, db_url=None):
        
        self.db_manager = DatabaseManager(db_url if db_url is not None else DATABASE_URL)
        self.report_manager = ReportManager(self.db_manager)
        self.interactive_mode = InteractiveMode(self.db_manager)

    def main_menu(self):
        while True:
            print("\nManager Terminal:")
            print("  1. Interactive Mode")
            print("  2. Report Management")
            print("  3. Generate Provider Directory")
            print("  4. Exit\n")
            choice = prompt_until_valid(
                r'^[1-4]$',
                ">> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Interactive Mode
                self.interactive_mode.main_menu()
            elif choice == "2": # Report Management
                self.report_management_menu()
            elif choice == "3": # Generate Provider Directory
                self.report_manager.generate_provider_directory()
            elif choice == "4": # Exit
                print("\nExiting... Goodbye!")
            else: # Catch all
                print("\nError occurred. Exiting...")

    def report_management_menu(self):
        while True:
            print("\nManager Terminal:")
            print("  Report Management:")
            print("    1. Main Accounting Procedure")
            print("    2. Generate Summary Report")
            print("    3. Generate Member Report")
            print("    4. Generate Provider Report")
            print("    5. Generate EFT Data")
            print("    6. Go Back")
            print("    7. Exit\n")
            choice = prompt_until_valid(
                r'^[1-7]$',
                ">> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1": # Main Accounting Procedure
                print("\nRunning main acccounting procedure...")
                self.report_manager.main_accounting_procedure()
            elif choice == "2": # Generate Summary Report
                print("\nGenerating summary report...")
                self.report_manager.generate_summary_report()
            elif choice == "3": # Gemerate Member Report
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter member number: ",
                    "Member number must be 9 digits."
                )
                print("\nGenerating member report...")
                self.report_manager.generate_member_report(member_number)
            elif choice == "4":  # Generate Provider Report
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    ">> Enter provider number: ",
                    "Provider number must be 9 digits."
                )
                print("\nGenerating provider report...")
                self.report_manager.generate_provider_report(provider_number)
            elif choice == "5":  # Generate EFT Data
                self.report_manager.generate_eft_data()
            elif choice == "6": # Go Back
                return
            elif choice == "7": # Exit
                print("Exiting... Goodbye!")
                sys.exit(0)
            else:
                print("Error occurred. Exiting...")
                sys.exit(1)

    def start(self):
        self.main_menu()
