from app.models import Base
from app.database import engine  # Import your SQLAlchemy engine

print("Tables in Base.metadata:")
for table_name in Base.metadata.tables.keys():
    print(table_name)

# Optional: Test table creation SQL for `DBProposal`
from sqlalchemy.schema import CreateTable
from app.models.proposals import DBProposal

print("\nGenerated SQL for DBProposal table:")
print(CreateTable(DBProposal.__table__).compile(engine))
