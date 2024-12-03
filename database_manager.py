# from sqlalchemy import create_engine 
# from sqlalchemy.orm import sessionmaker, Session
# from contextlib import contextmanager
# from models import Base

# engine = create_engine('sqlite:///chocan.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)

# @contextmanager
# def get_session():
#     session = Session()
#     try:
#         yield session  # Provide the session to the calling code
#         session.commit()  # Commit changes
#     except Exception as e:
#         session.rollback()  # Rollback on error
#         raise e
#     finally:
#         session.close()  # Always close the session


from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
from models import Base
from contextlib import contextmanager

# Defines the database URL
DATABASE_URL = "sqlite:///chocan.db"

# Handles Database Setup
class DatabaseManager:
    def __init__(self, db_url=None):
        """
        Initialize the database manager with a database URL.
        If no URL is provided, defaults to the global DATABASE_URL.
        """
        self.engine = create_engine(db_url or DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        # Initialize the database manager with the default DATABASE_URL
        db_manager = DatabaseManager()

        # Perform database operations
        with db_manager.get_session() as session:
            # Example: Add a record to the database
            new_member = Member(
                name="John Doe",
                street_address="123 Elm St",
                city="Metropolis",
                state="NY",
                zip_code="12345",
                is_active=1
            )
            session.add(new_member)  # Add the record
            print("Member added successfully!")
        """
        session = self.Session()
        try:
            yield session  # Provide the session to the calling code
            session.commit()  # Commit changes
        except Exception as e:
            session.rollback()  # Rollback on error
            raise e
        finally:
            session.close()  # Always close the session
