from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from contextlib import contextmanager
from constants import DATABASE_URL



# Handles Database Setup
class DatabaseManager:
    def __init__(self, db_url=None):
        """
        Initialize the database manager with the provided database URL.
        Otherwise, defaults to the DATABASE_URL from constants file.
        """
        self.engine = create_engine(db_url or DATABASE_URL)
        Base.metadata.create_all(self.engine)
        # self.Session = sessionmaker(bind=self.engine)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    @contextmanager
    def get_session(self):
        """
        Initializes a session and yields it to the calling code.
        Commits changes if no exceptions are raised, otherwise rolls back.
        Always closes the session when done.

        ```python
        # Example Usage: add a record to the database
        db_manager = DatabaseManager()
        # Perform database operations within the context manager
        with db_manager.get_session() as session:
            new_member = Member(
                name="John Doe",
                street_address="123 Elm St",
                city="Metropolis",
                state="NY",
                zip_code="12345"
            )
            session.add(new_member)
        ```
        """
        session = self.Session()
        try:
            yield session  # Provide the session to the calling code
            session.commit()  # Commit changes
        except Exception as e:
            session.rollback()  # Rollback on error
            raise f"Error: {e}"
        finally:
            session.close()  # Always close the session



####################################
# From main.py - Delete when done
####################################
# engine = create_engine('sqlite:///chocan.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()

# Example Usage of get_session() from the DatabaseManager class


