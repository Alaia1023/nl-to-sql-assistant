from datetime import date
from decimal import Decimal

from src.finance_database import FinanceBase, finance_engine
from src.finance_models import (
    Fund,
    Portfolio,
    Security,
    Position,
    Transaction,
    NAVHistory,
)


def seed_database():
    FinanceBase.metadata.drop_all(bind=finance_engine)
    FinanceBase.metadata.create_all(bind=finance_engine)

    with __import__("sqlalchemy").orm.Session(finance_engine) as session:
        funds = [
            Fund(
                fund_id=1,
                fund_name="Global Equity Fund",
                strategy="Equity",
                inception_date=date(2020, 1, 15),
                currency="USD",
            ),
            Fund(
                fund_id=2,
                fund_name="European Bond Fund",
                strategy="Fixed Income",
                inception_date=date(2019, 6, 1),
                currency="EUR",
            ),
            Fund(
                fund_id=3,
                fund_name="Technology Growth Fund",
                strategy="Growth",
                inception_date=date(2021, 3, 10),
                currency="USD",
            ),
        ]

        portfolios = [
            Portfolio(
                portfolio_id=1,
                fund_id=1,
                portfolio_name="Global Equity Portfolio A",
                mandate="Global Equities",
                base_currency="USD",
            ),
            Portfolio(
                portfolio_id=2,
                fund_id=1,
                portfolio_name="Global Equity Portfolio B",
                mandate="Large Cap Equities",
                base_currency="USD",
            ),
            Portfolio(
                portfolio_id=3,
                fund_id=2,
                portfolio_name="European Bond Portfolio",
                mandate="European Bonds",
                base_currency="EUR",
            ),
            Portfolio(
                portfolio_id=4,
                fund_id=3,
                portfolio_name="Technology Portfolio",
                mandate="Technology Equities",
                base_currency="USD",
            ),
        ]

        securities = [
            Security(
                security_id=1,
                ticker="AAPL",
                security_name="Apple Inc.",
                asset_class="Equity",
                sector="Technology",
                currency="USD",
            ),
            Security(
                security_id=2,
                ticker="MSFT",
                security_name="Microsoft Corporation",
                asset_class="Equity",
                sector="Technology",
                currency="USD",
            ),
            Security(
                security_id=3,
                ticker="NVDA",
                security_name="NVIDIA Corporation",
                asset_class="Equity",
                sector="Technology",
                currency="USD",
            ),
            Security(
                security_id=4,
                ticker="NESN",
                security_name="Nestle SA",
                asset_class="Equity",
                sector="Consumer Staples",
                currency="CHF",
            ),
            Security(
                security_id=5,
                ticker="SAP",
                security_name="SAP SE",
                asset_class="Equity",
                sector="Technology",
                currency="EUR",
            ),
            Security(
                security_id=6,
                ticker="UST10Y",
                security_name="US Treasury 10Y Bond",
                asset_class="Bond",
                sector="Government",
                currency="USD",
            ),
            Security(
                security_id=7,
                ticker="BUND10Y",
                security_name="German Government 10Y Bond",
                asset_class="Bond",
                sector="Government",
                currency="EUR",
            ),
            Security(
                security_id=8,
                ticker="AMZN",
                security_name="Amazon.com Inc.",
                asset_class="Equity",
                sector="Consumer Discretionary",
                currency="USD",
            ),
        ]

        positions = [
            (1, 1, 1, "2026-10-31", "100", "250", "25000"),
            (2, 1, 2, "2026-10-31", "80", "400", "32000"),
            (3, 1, 4, "2026-10-31", "150", "120", "18000"),
            (4, 1, 8, "2026-10-31", "50", "200", "10000"),
            (5, 2, 1, "2026-10-31", "60", "250", "15000"),
            (6, 2, 3, "2026-10-31", "40", "180", "7200"),
            (7, 2, 5, "2026-10-31", "100", "210", "21000"),
            (8, 3, 6, "2026-10-31", "200", "980", "196000"),
            (9, 3, 7, "2026-10-31", "100", "950", "95000"),
            (10, 4, 1, "2026-10-31", "100", "250", "25000"),
            (11, 4, 2, "2026-10-31", "100", "400", "40000"),
            (12, 4, 3, "2026-10-31", "150", "180", "27000"),
            (13, 4, 5, "2026-10-31", "50", "210", "10500"),
            (14, 1, 1, "2026-09-30", "100", "240", "24000"),
            (15, 1, 2, "2026-09-30", "80", "390", "31200"),
            (16, 4, 3, "2026-09-30", "150", "170", "25500"),
        ]

        position_records = [
            Position(
                position_id=position_id,
                portfolio_id=portfolio_id,
                security_id=security_id,
                as_of_date=date.fromisoformat(as_of_date),
                quantity=Decimal(quantity),
                market_price=Decimal(market_price),
                market_value=Decimal(market_value),
            )
            for (
                position_id,
                portfolio_id,
                security_id,
                as_of_date,
                quantity,
                market_price,
                market_value,
            ) in positions
        ]

        transactions_data = [
            (1, 1, 1, "2026-10-02", "BUY", "20", "245", "5"),
            (2, 1, 2, "2026-10-05", "BUY", "10", "395", "5"),
            (3, 1, 4, "2026-10-08", "SELL", "15", "118", "4"),
            (4, 2, 3, "2026-10-10", "BUY", "25", "175", "6"),
            (5, 2, 5, "2026-10-12", "BUY", "30", "205", "5"),
            (6, 3, 6, "2026-10-15", "BUY", "50", "975", "10"),
            (7, 3, 7, "2026-10-18", "SELL", "10", "945", "8"),
            (8, 4, 3, "2026-10-20", "BUY", "40", "178", "7"),
            (9, 4, 1, "2026-10-22", "SELL", "10", "248", "5"),
            (10, 4, 2, "2026-10-25", "BUY", "15", "398", "5"),
            (11, 1, 8, "2026-09-15", "BUY", "20", "195", "4"),
            (12, 3, 6, "2026-09-20", "BUY", "30", "970", "8"),
        ]

        transaction_records = [
            Transaction(
                transaction_id=transaction_id,
                portfolio_id=portfolio_id,
                security_id=security_id,
                transaction_date=date.fromisoformat(transaction_date),
                transaction_type=transaction_type,
                quantity=Decimal(quantity),
                price=Decimal(price),
                fees=Decimal(fees),
            )
            for (
                transaction_id,
                portfolio_id,
                security_id,
                transaction_date,
                transaction_type,
                quantity,
                price,
                fees,
            ) in transactions_data
        ]

        nav_data = [
            (1, 1, "2026-09-30", "102.50", "100000", "10250000"),
            (2, 1, "2026-10-31", "105.20", "100000", "10520000"),
            (3, 2, "2026-09-30", "98.40", "80000", "7872000"),
            (4, 2, "2026-10-31", "99.10", "80000", "7928000"),
            (5, 3, "2026-09-30", "110.00", "50000", "5500000"),
            (6, 3, "2026-10-31", "111.50", "50000", "5575000"),
        ]

        nav_records = [
            NAVHistory(
                nav_id=nav_id,
                fund_id=fund_id,
                nav_date=date.fromisoformat(nav_date),
                nav_per_share=Decimal(nav_per_share),
                shares_outstanding=Decimal(shares_outstanding),
                total_nav=Decimal(total_nav),
            )
            for (
                nav_id,
                fund_id,
                nav_date,
                nav_per_share,
                shares_outstanding,
                total_nav,
            ) in nav_data
        ]

        session.add_all(funds)
        session.add_all(portfolios)
        session.add_all(securities)
        session.add_all(position_records)
        session.add_all(transaction_records)
        session.add_all(nav_records)

        session.commit()

    print("Financial database created successfully.")
    print("Funds: 3")
    print("Portfolios: 4")
    print("Securities: 8")
    print("Positions: 16")
    print("Transactions: 12")
    print("NAV history records: 6")


if __name__ == "__main__":
    seed_database()
