from database_manager import DatabaseManager
from models import Service

class ServiceManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add_service(self, name, fee):
        with self.db_manager.get_session() as session:
            new_service = Service(name=name, fee=fee)
            session.add(new_service)
            print(f">> Added service: {name} with code {new_service.code}")

    def update_service(self, service_code, **kwargs):
     with self.db_manager.get_session() as session:
            service = session.query(Service).filter_by(code=service_code).first()
        
            if not service:
                print(f"Service with code {service_code} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['code']:
                    setattr(service, key, value)
                    
            print(f">> Updated service with code {service_code}")

    def delete_service(self, service_code):
        with self.db_manager.get_session() as session:
            service = session.query(Service).filter_by(code=service_code).first()

            if not service:
                print(f"Service with code {service_code} not found.")
                return

            session.delete(service)
            print(f"Deleted service with code {service_code}")

    def view_services(self):
        with self.db_manager.get_session() as session:
            services = session.query(Service).all()
            for service in services:
                print(f"{service.code}: {service.name} - ${service.fee:.2f}")
