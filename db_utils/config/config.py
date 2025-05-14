import os

from dotenv import load_dotenv


class Config:
    def __init__(self, dotenv_path=".env"):
        load_dotenv(dotenv_path)
        # POSTGRESQL PARAMS
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", 5432))
        # RECONNECT PARAMS
        self.retries = int(os.getenv("RECONNECT_RETRIES", 3))
        self.backoff = int(os.getenv("RECONNECT_BACKOFF", 2))
        self.delay = int(os.getenv("RECONNECT_DELAY", 2))

    def as_dict(self):
        return {
            "host": self.db_host,
            "dbname": self.db_name,
            "user": self.db_user,
            "password": self.db_password,
        }
