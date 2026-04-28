import pandas as pd
from sqlalchemy import create_engine, text
from .config import DATABASE_URL, DATA_PATH


def get_engine():
    """Create a SQLAlchemy engine for PostgreSQL."""
    return create_engine(DATABASE_URL, pool_pre_ping=True)


def load_csv() -> pd.DataFrame:
    """Fallback data source when PostgreSQL is not configured."""
    return pd.read_csv(
        DATA_PATH,
        parse_dates=["po_date", "expected_delivery_date", "actual_delivery_date"]
    )


def read_sql(query: str) -> pd.DataFrame:
    """Run SQL against PostgreSQL."""
    engine = get_engine()
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)
