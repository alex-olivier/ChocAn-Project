from datetime import datetime
from chocan_software.models import Member
from chocan_software.models import Provider
from chocan_software.models import Service
from chocan_software.models import ServiceRecord
from chocan_software.data_managers.database_manager import DatabaseManager


class ServiceRecordManager:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager is not None else DatabaseManager()

    def add_service_record(self, provider_number, member_number, service_code, date_of_service, comments=None):
        provider_id = int(provider_number)
        member_id = int(member_number)
        service_id = int(service_code)

        with self.db_manager.get_session(commit=True) as session:
            provider = session.query(Provider).filter_by(id=provider_id).first()
            member = session.query(Member).filter_by(id=member_id).first()
            service = session.query(Service).filter_by(id=service_id).first()
            if not provider or not member or not service:
                print("\nInvalid provider, member, or service code.")
                return

            new_service_record = ServiceRecord(
                provider_id=provider.id,
                member_id=member.id,
                service_id=service.id,
                service_date=datetime.strptime(date_of_service, "%m-%d-%Y"),
                comments=comments
            )
            session.add(new_service_record)
            session.commit()
            print(f"\n>> Service recorded for {member.name} by {provider.name}")
    
    def update_service_record(self, record_id, **kwargs):
        record_id = int(record_id)
        with self.db_manager.get_session(commit=True) as session:
            record = session.query(ServiceRecord).filter_by(id=record_id).first()
            if not record:
                print(f"\nService record with ID {record_id} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['id']:
                    setattr(record, key, value)
            
            print(f"\nUpdated service record.")
        
    def delete_service_record(self, record_id):
        record_id = int(record_id)
        with self.db_manager.get_session(commit=True) as session:
            record = session.query(ServiceRecord).filter_by(id=record_id).first()
            if not record:
                print(f"\nService record with ID {record_id} not found.")
                return

            session.delete(record)
            print(f"\nDeleted service record.")
    
    def view_service_records(self):
        with self.db_manager.get_session() as session:
            records = session.query(ServiceRecord).all()
            if not records:
                print("\nNo service records found.")
            else:
                for record in records:
                    print(f"  {record.id:06}: {record.service_date} - {record.member.name:<25} - {record.service.name}")
    
    def is_valid_service_record(self, record_id):
        record_id = int(record_id)
        with self.db_manager.get_session() as session:
            record = session.query(ServiceRecord).filter_by(id=record_id).first()
            return record if record else None

    def get_service_record(self, record_id):
        record_id = int(record_id)
        with self.db_manager.get_session() as session:
            record = session.query(ServiceRecord).filter_by(id=record_id).first()
            return record if record else None
    
    def get_service_records_by_provider(self, provider_number):
        provider_id = int(provider_number)
        with self.db_manager.get_session() as session:
            records = session.query(ServiceRecord).filter_by(provider_id=provider_id).all()
            return records if records else None
    
    def get_service_records_by_member(self, member_number):
        member_id = int(member_number)
        with self.db_manager.get_session() as session:
            records = session.query(ServiceRecord).filter_by(member_id=member_id).all()
            return records if records else None

    # Uses strings for the start_ddate and end_date
    def get_service_records_by_date_range(self, start_date: str, end_date: str):
        start_date = datetime.strptime(start_date, "%m-%d-%Y")
        end_date = datetime.strptime(end_date, "%m-%d-%Y")
        with self.db_manager.get_session() as session:
            records = session.query(ServiceRecord).filter(
                ServiceRecord.service_date.between(start_date, end_date)
            ).all()
            return records if records else None
    
    # uses datetime objects instead of strings
    def query_service_records_by_date_range(self, start_date: datetime, end_date: datetime):
        with self.db_manager.get_session() as session:
            records = session.query(ServiceRecord).filter(
                ServiceRecord.service_date >= start_date,
                ServiceRecord.service_date <= end_date
            ).all()
            return records if records else None