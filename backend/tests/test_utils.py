from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.types import JSON

def adapt_model_to_sqlite(engine, model):
    """Adapt a model to use JSON instead of ARRAY for SQLite."""
    if engine.dialect.name == "sqlite":
        for column in model.__table__.columns:
            if isinstance(column.type, PG_ARRAY):
                column.type = JSON  # Replace ARRAY with JSON for SQLite
