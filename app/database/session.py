import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.environ['DATABASE_URL'], pool_pre_ping=True, max_overflow=-1)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=True, bind=engine)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
