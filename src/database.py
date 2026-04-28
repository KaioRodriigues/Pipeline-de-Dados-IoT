from sqlalchemy import create_engine

try:
    from .config import DATABASE_URL
except ImportError:
    from config import DATABASE_URL


def get_engine():
    return create_engine(DATABASE_URL)
