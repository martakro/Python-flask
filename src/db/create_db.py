from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings


def get_engine(user: str, password: str, host: str, port: int, db_name: str) -> Engine:
    """
    Creates engine
    """
    url = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(url, echo=True)


def get_engine_from_settings():
    """
    Creates engine from settings file
    """
    config = Settings()

    return get_engine(
        user=config.pguser,
        password=config.pgpassword,
        host=config.pghost,
        port=config.pgport,
        db_name=config.pgdb,
    )


engine = get_engine_from_settings()


def get_session():
    """
    Creates session
    """
    return sessionmaker(bind=engine)()
