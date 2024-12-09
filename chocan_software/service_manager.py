from chocan_software.database_manager import DatabaseManager
from chocan_software.models import Service

class ServiceManager:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager is not None else DatabaseManager()

    def add_service(self, name, fee):
        with self.db_manager.get_session(commit=True) as session:
            new_service = Service(name=name, fee=fee)
            session.add(new_service)
            print(f"\nAdded service.")

    def update_service(self, service_code, **kwargs):
        service_id = int(service_code)
        with self.db_manager.get_session(commit=True) as session:
            service = session.query(Service).filter_by(id=service_id).first()
        
            if not service:
                print(f"\nService with code {service_code} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['code']:
                    setattr(service, key, value)
                    
            print(f"\nUpdated service.")

    def delete_service(self, service_code):
        service_id = int(service_code)
        with self.db_manager.get_session(commit=True) as session:
            service = session.query(Service).filter_by(id=service_id).first()

            if not service:
                print(f"\nService with code {service_code} not found.")
                return

            session.delete(service)
            print(f"\nDeleted service.")

    def view_services(self):
        with self.db_manager.get_session() as session:
            services = session.query(Service).all()
            if not services:
                print("\nNo services found.")
            else:
                for service in services:
                    print(f"  {service.id:06}: {service.name:<20} - ${service.fee:6.2f}")
