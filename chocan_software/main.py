import sys
from chocan_software.manager_terminal import ManagerTerminal
from chocan_software.provider_terminal import ProviderTerminal
from chocan_software.string_utils import prompt_until_valid
from chocan_software.constants import DATABASE_URL

def main_menu(provider_terminal: ProviderTerminal, manager_terminal: ManagerTerminal):
        print("\n------------------------------")
        print("Main Menu")
        print("------------------------------")
        print("  1. Provider Terminal")
        print("  2. Manager Terminal")
        print("  3. Exit")

        choice = prompt_until_valid(
            r'^[1-3]$',
            "\n>> Enter your choice: ",
            "Invalid choice. Please try again."
        )
        if choice == "1":  # Provider Terminal
            provider_terminal.run()
        elif choice == "2":  # Manager Terminal
            manager_terminal.run()
        elif choice == "3":  # Exit
            print("\nExiting... Goodbye!")
            sys.exit(0)
        else:  # Catch all
            print("\nError occurred. Exiting...")
            sys.exit(1)

if __name__ == "__main__":
    provider_terminal = ProviderTerminal(DATABASE_URL)
    manager_terminal = ManagerTerminal(DATABASE_URL)
    main_menu(provider_terminal, manager_terminal)



# # Example ussage
# if __name__ == "__main__":

#     print("\n---- ChocAn Data Processing System ----")
#     print("[1] Interactive Mode")
#     print("[2] Manager Terminal")
#     print("[3] Provider Terminal")
#     print("[4] Generate EFT Data")
#     print("[5] Generate Provider Directory")
#     interactive_mode = InteractiveMode()

#     add_member("John Doe", "123456789", "123 Main St", "Anytown", "CA", "90210")
#     add_provider("Dr. Smith", "987654321", "456 Elm St", "Othertown", "NY", "10001")
#     add_service("598470", "Dietitian Session", 150.00)
#     record_service("987654321", "123456789", "598470", "11-24-2024", "Initial consultation")

#     # Example usage of additional functionalities
#     generate_member_report("123456789")
#     generate_provider_report("987654321")
#     # generate_eft_data()
#     generate_summary_report()
