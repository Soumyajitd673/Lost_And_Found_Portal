import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()


def create_database():
    url = URL.create(
        drivername="mysql+pymysql",
        username=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306"))
    )

    engine = create_engine(url)

    with engine.connect() as connection:
        connection.exec_driver_sql(
            f"CREATE DATABASE IF NOT EXISTS `{os.getenv('DB_NAME')}`"
        )

    engine.dispose()