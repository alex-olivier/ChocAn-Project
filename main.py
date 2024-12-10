import sys
from chocan_software.user_terminals.manager_terminal import ManagerTerminal
from chocan_software.user_terminals.provider_terminal import ProviderTerminal
from chocan_software.string_utils import prompt_until_valid
from chocan_software.constants import DATABASE_URL


def acceptance_test_menu(provider_terminal: ProviderTerminal, manager_terminal: ManagerTerminal):
    print("╔═══════════════════════════╗")
    print("║  Acceptance Testing Menu  ║")
    print("╚═══════════════════════════╝")
    print("  1. Provider Terminal")
    print("  2. Manager Terminal")
    print("  3. Exit\n")
    choice = prompt_until_valid(
        r'^[1-3]$',
        ">> Enter your choice: ",
        "Invalid choice. Please try again."
    )
    if choice == "1": # Provider Terminal
        provider_terminal.start()
    elif choice == "2": # Manager Terminal
        manager_terminal.start()
    elif choice == "3": # Exit
        print("\nExiting... Goodbye!")
        sys.exit(0)
    else:  # Catch all
        print("\nError occurred. Exiting...")
        sys.exit(1)

if __name__ == "__main__":
    provider_terminal = ProviderTerminal(DATABASE_URL)
    manager_terminal = ManagerTerminal(DATABASE_URL)
    acceptance_test_menu(provider_terminal, manager_terminal)
