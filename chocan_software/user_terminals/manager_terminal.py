import sys
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.report_manager import ReportManager
from chocan_software.data_managers.service_manager import ServiceManager
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
        self.service_manager = ServiceManager(self.db_manager)

    def main_menu(self):
            print("\nManager Terminal:")
            print("  1. Interactive Mode")
            print("  2. Report Management")
            print("  3. Generate Provider Directory")
            print("  4. Exit")

            choice = prompt_until_valid(
                r'^[1-4]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":  # Interactive Mode
                 self.interactive_mode.run()
            elif choice == "2":  # Report Management
                self.report_management()
            elif choice == "3":  # Generate Provider Directory
                self.service_manager.view_services()
                pass
            elif choice == "4":
                print("Exiting... Goodbye!")
            else: # Catch all
                print("Error occurred. Exiting...")

    def report_management(self):
            print("\nManager Terminal:")
            print("  Report Management:")
            print("    1. Main accounting procedure")
            print("    2. Generate Summary Report")
            print("    3. Generate Member Report")
            print("    4. Generate Provider Report")
            print("    5. Generate EFT Data")
            print("    6. Exit")

            choice = prompt_until_valid(
                r'^[1-4]$',
                "\n>> Enter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":  # Main Accounting Procedure
                print("\nRunning main acccounting procedure...")
                self.report_manager.main_accounting_procedure()
            elif choice == "2":  # Generate Summary Report
                print("\nGenerating summary report...")
                self.report_manager.generate_summary_report()
            elif choice == "3":  # Gemerate Member Report
                print("\nGenerating member report...")
                member_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    "\n>> Enter member number: ",
                    "Member number must be 9 digits."
                )
                self.report_manager.generate_member_report(member_number)
            elif choice == "4":  # Generate Provider Report
                print("\nGenerating provider report...")
                provider_number = prompt_until_valid(
                    rf'^\d{{{ACCOUNT_NUM_LEN}}}$',
                    "\n>> Enter provider number: ",
                    "Provider number must be 9 digits."
                )
                self.report_manager.generate_provider_report(provider_number)
            elif choice == "5":  # Generate EFT Data
                self.report_manager.generate_eft_data()
            elif choice == "6":
                print("Exiting... Goodbye!")
                return
            else:
                print("Error occurred. Exiting...")
                sys.exit(1)

    def run(self):
            self.main_menu()