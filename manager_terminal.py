from input_validation import prompt_until_valid
from report_manager import ReportManager

class ManagerTerminal:
# TODO: Fix manager_terminal() to call the correct functions
    def main_menu():
            print("\n---------------------------------------------------")
            print("Manager Terminal")
            print("---------------------------------------------------")
            print("Manager Terminal:")
            print("  1. Report Management")
            print("  2. Generate EFT Data")
            print("  3. Generate Provider Directory")
            print("  4. Exit")
            choice = prompt_until_valid(
                r'^[1-4]$',
                "\nEnter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":
                pass  # Report Management
            elif choice == "2":
                pass  # Generate EFT Data
            elif choice == "3":
                pass  # Generate Provider Directory
            elif choice == "4":
                print("Exiting... Goodbye!")
            else:
                print("Error occurred. Exiting...")

    # TODO: Fix report_management() to call the correct functions
    def report_management():
            report_manager = ReportManager()
            print("\n---------------------------------------------------")
            print("Manager Terminal > Report Management")
            print("---------------------------------------------------")
            print("Manager Terminal:")
            print("  Report Management:")
            print("    1. Main Accounting Procedure")
            print("    2. Generate Summary Report")  
            print("    3. Generate Member Report")
            print("    4. Generate Provider Report")
            print("    5. Exit")
            choice = prompt_until_valid(
                r'^[1-4]$',
                "\nEnter your choice: ",
                "Invalid choice. Please try again."
            )
            if choice == "1":
                pass  # Main Accounting Procedure
            elif choice == "2":
                pass  # Generate Summary Report
            elif choice == "3":
                member_number = prompt_until_valid(
                    r'^\d{9}$',
                    "\nEnter member number: ",
                    "Member number must be 9 digits."
                )
                report_manager.generate_member_report(member_number)
            elif choice == "4":
                provider_number = prompt_until_valid(
                    r'^\d{9}$',
                    "\nEnter provider number: ",
                    "Provider number must be 9 digits."
                )
                report_manager.generate_provider_report(provider_number)
            elif choice == "5":
                print("Exiting... Goodbye!")
            else:
                print("Error occurred. Exiting...")
