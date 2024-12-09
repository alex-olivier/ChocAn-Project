from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from chocan_software.models import Base
from chocan_software.constants import DATABASE_URL

# Handles Database Setup
class DatabaseManager:
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


# PyTest Version of Code
"""
# Handles Database Setup
class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self, commit=False):
        Session = self.Session
        try:
            yield Session
            if commit:
                Session.commit()
        except Exception as e:
            Session.rollback()
            raise e
        finally:
            Session.close()
"""

# Original Version of Code
"""
    # DEBUGGING #############################
    # import logging
    # logging.basicConfig(level=logging.INFO)
    # logger = logging.getLogger(__name__)
    #########################################

    # Handles Database Setup
    class DatabaseManager:
        def __init__(self, db_url=None):
            # Initialize the database manager with the provided database URL.
            # Otherwise, defaults to the DATABASE_URL from constants file.

            self.engine = create_engine(db_url if db_url is not None else DATABASE_URL)
            Base.metadata.create_all(self.engine)
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            # self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine) # try this one?
            # self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self, commit=False):
        # Context manager to provide a session for database operations
        # commit (bool): Whether to automatically commit changes after the session.
        #                Defaults to False for read-only or manual commit control.

        session = self.session
        # logger.info("Session started.") # DEBUGGING
        try:
            yield session  # Provide the session to the caller
            if commit:  # Commit only if explicitly requested
                session.commit()
                # logger.info("Session committed.") # DEBUGGING
        except Exception as e:
            session.rollback()  # Rollback on error
            # logger.error("Session rolled back due to an exception.", exc_info=True) # DEBUGGING
            raise e
        finally:
            session.close()  # Always close the session
            # logger.info("Session closed.") # DEBUGGING
"""