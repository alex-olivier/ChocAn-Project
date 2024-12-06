from models import Member, Provider, Service, ServiceRecord
from database_manager import DatabaseManager

from datetime import datetime


# For the EFT data, all that is required is that a file be set up containing
# the provider name, provider number, and the amount to be transferred.
class EFTManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def generate_eft_data(self):
        with self.db_manager.get_session() as session:
            providers = session.query(Provider).all()
            eft_filename = f"EFT_Data_{datetime.now().strftime('%Y%m%d')}.txt"
            with open(eft_filename, 'w') as file:
                file.write("Provider EFT Data:\n")
                file.write("Provider Name, Provider Number, Total Fee\n")
                for provider in providers:
                    records = session.query(ServiceRecord).filter_by(provider_id=provider.id).all()
                    total_fee = sum(session.query(Service).filter_by(code=record.service_code).first().fee for record in records)
                    if total_fee > 0:
                        file.write(f"{provider.name}, {provider.number}, ${total_fee:.2f}\n")
            print(f"EFT data generated: {eft_filename}")
