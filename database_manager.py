from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from contextlib import contextmanager
from constants import DATABASE_URL

# DEBUGGING #############################
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
#########################################

# Handles Database Setup
class DatabaseManager:
    def __init__(self, db_url=None):
        """
        Initialize the database manager with the provided database URL.
        Otherwise, defaults to the DATABASE_URL from constants file.
        """
        self.engine = create_engine(db_url or DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def get_session(self, commit=False):
        """
        Context manager to provide a session for database operations
        commit (bool): Whether to automatically commit changes after the session.
                       Defaults to False for read-only or manual commit control.
        """
        session = self.Session()
        logger.info("Session started.") # DEBUGGING
        try:
            yield session  # Provide the session to the caller
            if commit:  # Commit only if explicitly requested
                session.commit()
                logger.info("Session committed.") # DEBUGGING
        except Exception as e:
            session.rollback()  # Rollback on error
            logger.error("Session rolled back due to an exception.", exc_info=True) # DEBUGGING
            raise e
        finally:
            session.close()  # Always close the session
            logger.info("Session closed.") # DEBUGGING

    # @contextmanager
    # def get_session(self):
    #     session = self.Session()
    #     try:
    #         yield session  # Provide the session to the calling code
    #         session.commit()  # Commit changes
    #     except Exception as e:
    #         session.rollback()  # Rollback on error
    #         raise e
    #     finally:
    #         session.close()  # Always close the session
