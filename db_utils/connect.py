import time

import psycopg2

from db_utils.config.config import Config
from db_utils.util.logger import logger


def connect(config: Config):
    """Try to connect to PostgreSQL with retry logic."""
    attempt = 1
    while attempt <= config.retries:
        try:
            conn = psycopg2.connect(**config.as_dict())
            logger.info(f"Connected to PostgreSQL on attempt {attempt}.")
            return conn
        except psycopg2.OperationalError as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            if attempt == config.retries:
                logger.error("All connection attempts failed.")
                raise
            sleep_time = config.delay * (config.backoff ** (attempt - 1))
            logger.info(f"Retrying in {sleep_time:.1f} seconds...")
            time.sleep(sleep_time)
            attempt += 1
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise
    return None
