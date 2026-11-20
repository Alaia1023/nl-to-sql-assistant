FINANCE_DATABASE_SCHEMA = """
Database: Financial Services and Asset Management

Table: funds
- fund_id INTEGER PRIMARY KEY
- fund_name VARCHAR(150)
- strategy VARCHAR(100)
- inception_date DATE
- currency VARCHAR(3)

Table: portfolios
- portfolio_id INTEGER PRIMARY KEY
- fund_id INTEGER FOREIGN KEY REFERENCES funds(fund_id)
- portfolio_name VARCHAR(150)
- mandate VARCHAR(100)
- base_currency VARCHAR(3)

Table: securities
- security_id INTEGER PRIMARY KEY
- ticker VARCHAR(20)
- security_name VARCHAR(150)
- asset_class VARCHAR(50)
- sector VARCHAR(100)
- currency VARCHAR(3)

Table: positions
- position_id INTEGER PRIMARY KEY
- portfolio_id INTEGER FOREIGN KEY REFERENCES portfolios(portfolio_id)
- security_id INTEGER FOREIGN KEY REFERENCES securities(security_id)
- as_of_date DATE
- quantity NUMERIC(20,6)
- market_price NUMERIC(20,6)
- market_value NUMERIC(20,2)

Table: transactions
- transaction_id INTEGER PRIMARY KEY
- portfolio_id INTEGER FOREIGN KEY REFERENCES portfolios(portfolio_id)
- security_id INTEGER FOREIGN KEY REFERENCES securities(security_id)
- transaction_date DATE
- transaction_type VARCHAR(10) -- BUY or SELL
- quantity NUMERIC(20,6)
- price NUMERIC(20,6)
- fees NUMERIC(20,2)

Table: nav_history
- nav_id INTEGER PRIMARY KEY
- fund_id INTEGER FOREIGN KEY REFERENCES funds(fund_id)
- nav_date DATE
- nav_per_share NUMERIC(20,6)
- shares_outstanding NUMERIC(20,2)
- total_nav NUMERIC(20,2)

Relationships:
- funds.fund_id = portfolios.fund_id
- funds.fund_id = nav_history.fund_id
- portfolios.portfolio_id = positions.portfolio_id
- securities.security_id = positions.security_id
- portfolios.portfolio_id = transactions.portfolio_id
- securities.security_id = transactions.security_id
"""
