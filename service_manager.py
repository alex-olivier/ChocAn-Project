from database_manager import DatabaseManager
from models import Service

class ServiceManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def add_service(self, name, fee):
        with self.db_manager.get_session() as session:
            new_service = Service(name=name, fee=fee)
            session.add(new_service)
            print(f"Added service: {name} with code {new_service.code}")


    # TODO: implement update_service() in ServiceManager class
    def update_service(self):
        pass


    # TODO: implment delete_service() in ServiceManager class
    def delete_service(self):
        pass


    # TODO: implement view_services() in ServiceManager class
    def view_services(self):
        with self.db_manager.get_session() as session:
            services = session.query(Service).all()
            for service in services:
                print(f"{service.code}: {service.name} - ${service.fee:.2f}")

"""
    # USE AS REFERENCE
    def add_person(self, person_class, name, street_address, city, state, zip_code):
        with self.db_manager.get_session() as session:
            new_person = person_class(
                name=name, 
                street_address=street_address, 
                city=city, 
                state=state, 
                zip_code=zip_code
            )
            session.add(new_person)
            print(f"Added {person_class.__name__.lower()}: {name}")

    def update_person(self, person_class, person_id, **kwargs):
        with self.db_manager.get_session() as session:
            person = session.query(
                person_class
            ).filter_by(
                id=person_id
            ).first()
            
            if not person:
                print(f"{person_class.__name__.lower()} with id {person_id} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['id', 'number']:
                    setattr(person, key, value)
                    
            print(f"Updated {person_class.__name__.lower()} with id {person_id}")

    def delete_person(self, person_class, person_id):
        with self.db_manager.get_session() as session:
            person = session.query(
                person_class
            ).filter_by(
                id=person_id
            ).first()

            if not person:
                print(f"{person_class.__name__.lower()} with id {person_id} not found.")
                return

            session.delete(person)
            print(f"Deleted {person_class.__name__.lower()} with id {person_id}")
"""


# # From main.py - Delete when done

# def add_service(name, fee):
#     service = Service(name=name, fee=fee)
#     session.add(service)
#     session.commit()
#     print(f"Added service: {name} with code {service.code}")