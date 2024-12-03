from models import Service
import re
from constants import (
    SERVICE_NAME_MAX_LEN,
    SERVICE_FEE_MAX
)

class ServiceManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_service(self):
        name, fee = self.prompt_service_details()

        with self.db_manager.get_session() as session:
            new_service = Service(name=name, fee=fee)
            session.add(new_service)
            print(f"Added service: {name} with code {new_service.code}")