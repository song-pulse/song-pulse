import logging

from app.database.init_db import init_db
from app.database.session import db_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init():
    init_db(db_session)


def main():
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
