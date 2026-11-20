from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

BASE_DIR = Path(__file__).resolve().parent.parent
FINANCE_DATABASE_PATH = BASE_DIR / "data" / "finance.db"

finance_engine = create_engine(
    f"sqlite:///{FINANCE_DATABASE_PATH}",
    echo=False
)


class FinanceBase(DeclarativeBase):
    pass
