
from backend.models import create_tables, get_engine

print("Creating/updating database tables...")
engine = get_engine()
create_tables(engine)
print("Database tables created successfully!")
