
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


# Get the project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define the SQLite database path
DATABASE_PATH = BASE_DIR / "data" / "shop.db"

# Create the database engine
engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    echo=True
)


# Define the base class for database models
class Base(DeclarativeBase):
    pass
