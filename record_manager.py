from models import Member, Provider, Service, ServiceRecord
from database_manager import DatabaseManager
from datetime import datetime

class RecordManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    # TODO: Finish implementing this method and make it work outside of main.py
    def record_service(self, provider_number, member_number, service_code, service_date, comments=None):
        with self.db_manager.get_session() as session:
            provider = session.query(Provider).filter_by(number=provider_number).first()
            member = session.query(Member).filter_by(number=member_number).first()
            service = session.query(Service).filter_by(code=service_code).first()

            if not provider or not member or not service:
                print("Invalid provider, member, or service code.")
                return

            new_service_record = ServiceRecord(
                provider_id=provider.id,
                member_id=member.id,
                service_code=service_code,
                service_date=datetime.datetime.strptime(service_date, "%m-%d-%Y"),
                comments=comments
            )
            session.add(new_service_record)
            session.commit()
            print(f"Service recorded for {member.name} by {provider.name}")



