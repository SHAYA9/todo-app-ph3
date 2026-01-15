from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# For local development, use SQLite if DATABASE_URL not set
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./todo_app.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """Get database session"""
    with Session(engine) as session:
        yield session