from database_manager import DatabaseManager
import re

# Handles Person Management
class PersonManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_person(self, person_class, name, street_address, city, state, zip_code):
        with self.db_manager.get_session() as session:
            new_person = person_class(name=name,
                                     street_address=street_address,
                                     city=city,
                                     state=state,
                                     zip_code=zip_code)

            session.add(new_person)
            print(f"Added {person_class.__name__.lower()}: {name}")

    def update_person(self, person_class, person_id, **kwargs):
        with self.db_manager.get_session() as session:
            person = session.query(person_class).filter_by(id=person_id).first()
            if not person:
                print(f"{person_class.__name__.lower()} with id {person_id} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['id', 'number']:
                    setattr(person, key, value)
                    
            print(f"Updated {person_class.__name__.lower()} with id {person_id}")

    def delete_person(self, person_class, person_id):
        with self.db_manager.get_session() as session:
            person = session.query(person_class).filter_by(id=person_id).first()
            if not person:
                print(f"{person_class.__name__.lower()} with id {person_id} not found.")
                return

            session.delete(person)
            print(f"Deleted {person_class.__name__.lower()} with id {person_id}")


