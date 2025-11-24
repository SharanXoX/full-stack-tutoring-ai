from typing import Generator
from sqlalchemy.orm import sessionmaker
from backend.models import get_engine

ENGINE = get_engine()

SessionLocal = sessionmaker(
    bind=ENGINE,
    autoflush=False,
    autocommit=False
)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
