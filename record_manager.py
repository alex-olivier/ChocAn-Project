from models import Member, Provider, Service, ServiceRecord
from database_manager import DatabaseManager
from datetime import datetime


class RecordManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    # TODO: Finish implementing this method and make it work outside of main.py
    def record_service(self, provider_number, member_number, service_code, date_of_service, comments=None):
        provider_id = int(provider_number)
        member_id = int(member_number)
        service_id = int(service_code)

        with self.db_manager.get_session() as session:
            provider = session.query(Provider).filter_by(id=provider_id).first()
            member = session.query(Member).filter_by(id=member_id).first()
            service = session.query(Service).filter_by(id=service_id).first()
            if not provider or not member or not service:
                print("Invalid provider, member, or service code.")
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
            print(f"Service recorded for {member.name} by {provider.name}")
