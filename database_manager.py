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
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self):
        session = self.Session()
        try:
            yield session  # Provide the session to the calling code
            session.commit()  # Commit changes
        except Exception as e:
            session.rollback()  # Rollback on error
            raise f"Error: {e}"
        finally:
            session.close()  # Always close the session
