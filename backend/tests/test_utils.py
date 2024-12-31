from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.types import JSON
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql.sqltypes import Enum

def adapt_model_to_sqlite(engine, model):
    """Adapt a model to use JSON instead of ARRAY for SQLite."""
    if engine.dialect.name == "sqlite":
           for column in model.__table__.columns:
            # Replace PostgreSQL-specific ARRAY with JSON
            if isinstance(column.type, ARRAY):
                column.type = JSON()
            # Replace JSONB with JSON
            elif isinstance(column.type, JSONB):
                column.type = JSON()
            # Replace Enum with String
            elif isinstance(column.type, Enum):
                column.type = String()
