from datetime import datetime
from chocan_software.data_managers.database_manager import DatabaseManager
from chocan_software.data_managers.person_manager import MemberManager
from chocan_software.data_managers.person_manager import ProviderManager
from chocan_software.data_managers.service_manager import ServiceManager
from chocan_software.data_managers.service_record_manager import ServiceRecordManager


class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url)
        self.provider_manager = ProviderManager(self.db_manager)
        self.member_manager = MemberManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)
        self.service_record_manager = ServiceRecordManager(self.db_manager)
    
    @staticmethod
    def is_valid_date(date_string):
        """Validate date format."""
        try:
            datetime.strptime(date_string, "%m-%d-%Y")
            return True
        except ValueError:
            return False
    
    def start(self):
        """Start the provider terminal."""
        print("")
        while True:
            provider_number = input("").strip()
            if not self.provider_manager.is_valid_provider(provider_number):
                print("Invalid Provider #")
                continue

            self.handle_member_interaction(provider_number)

    def handle_member_interaction(self, provider_number):
        """Handle member-related operations."""
        while True:
            member_number = input("").strip()
            if not self.member_manager.is_valid_member(member_number):
                print("Invalid Number")
                continue

            member = self.member_manager.get_member(member_number)
            if not member.status:
                print("Member Suspended")
                continue

            print("Validated")
            self.handle_service_date(provider_number, member_number)

    def handle_service_date(self, provider_number, member_number):
        """Handle service-related operations."""
        while True:
            date_of_service = input("").strip()
            if not self.is_valid_date(date_of_service):
                print("Invalid Date")
                continue
            self.handle_service_code(provider_number, member_number, date_of_service)

    def handle_service_code(self, provider_number, member_number, date_of_service):
        while True:
            service_code = input("").strip()
            service = self.service_manager.get_service(service_code)
            if not service:
                print("Invalid Code")
                continue
            
            print(f"{service.name}")
            confirmation = input("Continue? (y/n): ").strip().lower()
            if confirmation not in ['y', 'n']:
                print("Invalid Input")
                continue
            elif confirmation == 'n':
                continue

            comments = input("").strip()
            self.service_record_manager.add_service_record(
                provider_number=provider_number,
                member_number=member_number,
                service_code=service_code,
                date_of_service=date_of_service,
                comments=comments
            )
            print(f"{service.fee}")
            break
