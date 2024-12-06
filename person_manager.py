from database_manager import DatabaseManager
from models import Member, Provider

# Handles Person Management
class PersonManager:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

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
        
    def view_persons(self, person_class):
        with self.db_manager.get_session() as session:
            persons = session.query(person_class).all()
            for person in persons:
                print(f": {person.name} {person.number}")

# Member Manager
class MemberManager(PersonManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)
    
    def add_member(self, name, street_address, city, state, zip_code):
        super().add_person(Member, name, street_address, city, state, zip_code)

    def update_member(self, member_id, **kwargs):
        super().update_person(Member, member_id, **kwargs)

    def delete_member(self, member_id):
        super().delete_person(Member, member_id)

    def view_members(self):
        super().view_persons(Member)

# Provider Manager
class ProviderManager(PersonManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)

    def add_provider(self, name, street_address, city, state, zip_code):
        super().add_person(Provider, name, street_address, city, state, zip_code)

    def update_provider(self, provider_id, **kwargs):
        super().update_person(Provider, provider_id, **kwargs)

    def delete_provider(self, provider_id):
        super().delete_person(Provider, provider_id)

    def view_providers(self):
        super().view_persons(Provider)

# # From main.py - Delete when done
# def add_member(name, street_address, city, state, zip_code):
#     try:
#         new_member = Member(name=name, street_address=street_address, city=city, state=state, zip_code=zip_code)
#         session.add(new_member)  # Triggers validation
#         session.commit()
#         print(f"Added member: {name}")
#     except ValueError as e:
#         print(e)

# def add_provider(name, street_address, city, state, zip_code):
#     try:
#         new_provider = Provider(name=name, street_address=street_address, city=city, state=state, zip_code=zip_code)
#         session.add(new_provider)
#         session.commit()
#         print(f"Added provider: {name}")
#     except ValueError as e:
#         print(e)