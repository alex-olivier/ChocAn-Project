import sys
from datetime import datetime
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
    def is_valid_member(self, member_number) -> bool:
        if (super().is_valid(Member, member_number) is True):
            member_id = int(member_number)
            with self.db_manager.get_session(commit=True) as session:
                member = session.query(Member).filter_by(id=member_id).first()
                if member.status:
                    print ("\nValidated")
                    return True
                else:
                    print ("\nMember Suspended")
                    return False        
        else:
            print("\nInvalid Number")
            return False
"""
class ProviderTerminal:
    def __init__(self, db_url=None):
        self.db_manager = DatabaseManager(db_url)
        self.provider_manager = ProviderManager(self.db_manager)
        self.member_manager = MemberManager(self.db_manager)
        self.service_manager = ServiceManager(self.db_manager)
        self.service_record_manager = ServiceRecordManager(self.db_manager)

    def start(self):
        """Start the provider terminal."""
        print("\nProvider Terminal is switched on.")
        while True:
            provider_number = input("\nProvider #").strip()
            if not self.provider_manager.is_valid_provider(provider_number):
                print("Invalid Number")
                continue

            print("\nTerminal Activated.")
            self.handle_member_interaction(provider_number)

    def handle_member_interaction(self, provider_number):
        """Handle member-related operations."""
        while True:
            member_number = input("\nEnter Member Number: ").strip()
            if not self.member_manager.is_valid_member(member_number):
                print("Invalid Number")
                continue

            member = self.member_manager.get_member(member_number)
            if not member.status:
                print("Member Suspended")
                continue

            print("Validated")
            self.handle_service_interaction(provider_number, member_number)

    def handle_service_interaction(self, provider_number, member_number):
        """Handle service-related operations."""
        while True:
            date_of_service = input("\nEnter Date of Service (MM-DD-YYYY): ").strip()
            if not self.is_valid_date(date_of_service):
                print("Invalid Date")
                continue

            service_code = input("\nEnter Service Code: ").strip()
            service = self.service_manager.get_service(service_code)
            if not service:
                print("Invalid Code")
                continue

            print(f"Service Name: {service.name}")
            confirmation = input("\nIs this correct? (y/n): ").strip().lower()
            if confirmation not in ['y', 'n']:
                print("Invalid Input. Enter 'y' for Yes or 'n' for No.")
                continue
            elif confirmation == 'n':
                continue

            comments = input("\nEnter Comments (optional): ").strip()
            self.add_service_record(provider_number, member_number, service_code, date_of_service, comments)
            print("Service Record Added")
            break

    def add_service_record(self, provider_number, member_number, service_code, date_of_service, comments):
        """Add a service record."""
        self.service_record_manager.add_service_record(
            provider_number=provider_number,
            member_number=member_number,
            service_code=service_code,
            date_of_service=date_of_service,
            comments=comments
        )

    @staticmethod
    def is_valid_date(date_string):
        """Validate date format."""
        try:
            datetime.strptime(date_string, "%m-%d-%Y")
            return True
        except ValueError:
            return False
