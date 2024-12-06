from input_validation import prompt_until_valid

# TODO: Fix provider_terminal() to call the correct functions
def provider_terminal():
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
            pass  # Validate Member
        elif choice == "2":
            pass  # Record Service
        elif choice == "3":
            pass  # View Provider Directory
        elif choice == "4":
            print("Exiting... Goodbye!")
        else:
            print("Error occurred. Exiting...")

