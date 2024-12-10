from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chocan_software.models import Base
from chocan_software.constants import DATABASE_URL


class DatabaseManager:
    """
    Handles database setup and provides sessions for database operations.
    """
    def __init__(self, db_url=None):
        """
        Initialize the database manager with the provided database URL.
        Otherwise, defaults to the DATABASE_URL from constants file.
        """
        self.engine = create_engine(db_url if db_url is not None else DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # self.Session = sessionmaker(bind=self.engine)  # w/o autocommit and autoflush set to False

    @contextmanager
    def get_session(self, commit=False):
        """
        Context manager to provide a session for database operations
        commit (bool): Whether to automatically commit changes after the session.
                       Defaults to False for read-only or manual commit control.
        """
        session = self.Session()
        try:
            yield session  # Provide the session to the caller
            if commit:  # Commit only if explicitly requested
                session.commit()
        except Exception as e:
            session.rollback()  # Rollback on error
            raise e
        finally:
            session.close()  # Always close the session
