from database_manager import DatabaseManager, get_session
from models import Service
from input_validation import prompt_until_valid

class ServiceManager:
    def __init__(self, db_manager : DatabaseManager):
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
        pass



# # From main.py - Delete when done

# def add_service(name, fee):
#     service = Service(name=name, fee=fee)
#     session.add(service)
#     session.commit()
#     print(f"Added service: {name} with code {service.code}")