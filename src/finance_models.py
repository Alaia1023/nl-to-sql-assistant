from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.finance_database import FinanceBase


class Fund(FinanceBase):
    __tablename__ = "funds"

    fund_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_name: Mapped[str] = mapped_column(String(150), nullable=False)
    strategy: Mapped[str] = mapped_column(String(100), nullable=False)
    inception_date: Mapped[date] = mapped_column(Date, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    portfolios: Mapped[list["Portfolio"]] = relationship(
        back_populates="fund"
    )
    nav_history: Mapped[list["NAVHistory"]] = relationship(
        back_populates="fund"
    )


class Portfolio(FinanceBase):
    __tablename__ = "portfolios"

    portfolio_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_id: Mapped[int] = mapped_column(
        ForeignKey("funds.fund_id"),
        nullable=False
    )
    portfolio_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    mandate: Mapped[str] = mapped_column(String(100), nullable=False)
    base_currency: Mapped[str] = mapped_column(String(3), nullable=False)

    fund: Mapped["Fund"] = relationship(back_populates="portfolios")
    positions: Mapped[list["Position"]] = relationship(
        back_populates="portfolio"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="portfolio"
    )


class Security(FinanceBase):
    __tablename__ = "securities"

    security_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )
    security_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
    asset_class: Mapped[str] = mapped_column(String(50), nullable=False)
    sector: Mapped[str] = mapped_column(String(100), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)

    positions: Mapped[list["Position"]] = relationship(
        back_populates="security"
    )
    transactions: Mapped[list["Transaction"]] = relationship(
        back_populates="security"
    )


class Position(FinanceBase):
    __tablename__ = "positions"

    position_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.portfolio_id"),
        nullable=False
    )
    security_id: Mapped[int] = mapped_column(
        ForeignKey("securities.security_id"),
        nullable=False
    )
    as_of_date: Mapped[date] = mapped_column(Date, nullable=False)
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False
    )
    market_price: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False
    )
    market_value: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        nullable=False
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="positions"
    )
    security: Mapped["Security"] = relationship(
        back_populates="positions"
    )

    __table_args__ = (
        UniqueConstraint(
            "portfolio_id",
            "security_id",
            "as_of_date",
            name="uq_position_portfolio_security_date"
        ),
        CheckConstraint("quantity >= 0", name="ck_position_quantity"),
        CheckConstraint("market_value >= 0", name="ck_position_market_value"),
    )


class Transaction(FinanceBase):
    __tablename__ = "transactions"

    transaction_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    portfolio_id: Mapped[int] = mapped_column(
        ForeignKey("portfolios.portfolio_id"),
        nullable=False
    )
    security_id: Mapped[int] = mapped_column(
        ForeignKey("securities.security_id"),
        nullable=False
    )
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    transaction_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )
    quantity: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False
    )
    price: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False
    )
    fees: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        nullable=False
    )

    portfolio: Mapped["Portfolio"] = relationship(
        back_populates="transactions"
    )
    security: Mapped["Security"] = relationship(
        back_populates="transactions"
    )

    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('BUY', 'SELL')",
            name="ck_transaction_type"
        ),
        CheckConstraint("quantity > 0", name="ck_transaction_quantity"),
        CheckConstraint("price >= 0", name="ck_transaction_price"),
        CheckConstraint("fees >= 0", name="ck_transaction_fees"),
    )


class NAVHistory(FinanceBase):
    __tablename__ = "nav_history"

    nav_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fund_id: Mapped[int] = mapped_column(
        ForeignKey("funds.fund_id"),
        nullable=False
    )
    nav_date: Mapped[date] = mapped_column(Date, nullable=False)
    nav_per_share: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False
    )
    shares_outstanding: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        nullable=False
    )
    total_nav: Mapped[Decimal] = mapped_column(
        Numeric(20, 2),
        nullable=False
    )

    fund: Mapped["Fund"] = relationship(back_populates="nav_history")

    __table_args__ = (
        UniqueConstraint(
            "fund_id",
            "nav_date",
            name="uq_nav_fund_date"
        ),
        CheckConstraint("nav_per_share >= 0", name="ck_nav_per_share"),
        CheckConstraint("total_nav >= 0", name="ck_nav_total"),
    )
