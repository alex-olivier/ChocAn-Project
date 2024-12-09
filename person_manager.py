from database_manager import DatabaseManager
from models import Member, Provider


# The base class for managing ChocAn persons (members and providers)
class PersonManager:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager if db_manager is not None else DatabaseManager()

    def add_person(self, person_class, name, street_address, city, state, zip_code):
        with self.db_manager.get_session(commit=True) as session:
            new_person = person_class(
                name=name, 
                street_address=street_address, 
                city=city, 
                state=state, 
                zip_code=zip_code
            )
            session.add(new_person)
            print(f"\nAdded {person_class.__name__.lower()}.")

    def update_person(self, person_class, person_number, **kwargs):
        person_id = int(person_number)  # converting to int strips leading zeroes
        with self.db_manager.get_session(commit=True) as session:
            person = session.query(person_class).filter_by(
                id=person_id
            ).first()
            if not person:
                print(f"\n{person_class.__name__.lower()} with id {person_id:09} not found.")
                return

            for key, value in kwargs.items():
                if key not in ['id', 'number']:
                    setattr(person, key, value)
                    
            print(f"\nUpdated {person_class.__name__.lower()}.")

    def delete_person(self, person_class, person_number):
        person_id = int(person_number)  # converting to int strips leading zeroes
        with self.db_manager.get_session(commit=True) as session:
            person = session.query(person_class).filter_by(
                id=person_id
            ).first()
            if not person:
                print(f"\n{person_class.__name__.lower()} with id {person_id:09} not found.")
                return

            session.delete(person)
            print(f"\nDeleted {person_class.__name__.lower()}.")
        
    def view_persons(self, person_class):
        with self.db_manager.get_session() as session:
            persons = session.query(person_class).all()
            if not persons:
                print(f"\nNo {person_class.__name__.lower()}s found.")
            else:
                for person in persons:
                    print(f"{person.name}, {person.id:09}")

    def is_valid(self, person_class, person_number) -> bool:
        person_id = int(person_number)  # converting to int strips leading zeroes
        with self.db_manager.get_session() as session:
            person = session.query(person_class).filter_by(
                id=person_id
            ).first()
            return person is not None


# Handles the management of ChocAn members
class MemberManager(PersonManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)
    
    def add_member(self, name, street_address, city, state, zip_code):
        super().add_person(Member, name, street_address, city, state, zip_code)

    def update_member(self, member_number, **kwargs):
        super().update_person(Member, member_number, **kwargs)

    def delete_member(self, member_number):
        super().delete_person(Member, member_number)

    def view_members(self):
        super().view_persons(Member)

    def is_valid_member(self, member_number) -> bool:
        if (super().is_valid(Member, member_number) is True):
            member_id = int(member_number)
            with self.db_manager.get_session(commit=True) as session:
                member = session.query(Member).filter_by(id=member_id).first()
                if member.is_valid:
                    print ("\n🟢 Validated")
                    return True
                else:
                    print ("\n🔴 Member Suspended")
                    return False        
        else:
            print("\n⚠ Invalid Number")
            return False

# Handles the management of ChocAn providers
class ProviderManager(PersonManager):
    def __init__(self, db_manager):
        super().__init__(db_manager)

    def add_provider(self, name, street_address, city, state, zip_code):
        super().add_person(Provider, name, street_address, city, state, zip_code)

    def update_provider(self, provider_number, **kwargs):
        super().update_person(Provider, provider_number, **kwargs)

    def delete_provider(self, provider_number):
        super().delete_person(Provider, provider_number)

    def view_providers(self):
        super().view_persons(Provider)
    
    def is_valid_provider(self, provider_number) -> bool:
        return super().is_valid(Provider, provider_number)
