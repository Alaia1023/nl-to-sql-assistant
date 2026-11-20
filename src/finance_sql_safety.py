import sqlglot
from sqlglot import exp


FINANCE_ALLOWED_TABLES = {
    "funds",
    "portfolios",
    "securities",
    "positions",
    "transactions",
    "nav_history",
}


def validate_finance_read_only_sql(sql):
    if not isinstance(sql, str) or not sql.strip():
        raise ValueError("SQL query must be a non-empty string.")

    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except sqlglot.errors.ParseError as error:
        raise ValueError("Invalid SQL syntax.") from error

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    if not isinstance(statement, exp.Query):
        raise ValueError("Only read-only SELECT queries are allowed.")

    # CTE names are temporary query names, not physical database tables.
    cte_names = {
        cte.alias_or_name.lower()
        for cte in statement.find_all(exp.CTE)
    }

    referenced_tables = set()

    for table in statement.find_all(exp.Table):
        table_name = table.name.lower()

        # Reject qualified table references.
        if table.db or table.catalog:
            raise ValueError(
                "Qualified table references are not allowed."
            )

        # Ignore references to CTEs.
        if table_name not in cte_names:
            referenced_tables.add(table_name)

    if not referenced_tables.issubset(FINANCE_ALLOWED_TABLES):
        unauthorized = referenced_tables - FINANCE_ALLOWED_TABLES
        raise ValueError(
            f"Query references unauthorized tables: {sorted(unauthorized)}"
        )

    return True


if __name__ == "__main__":
    valid_sql = """
    WITH latest_nav AS (
        SELECT fund_id, MAX(nav_date) AS max_nav_date
        FROM nav_history
        GROUP BY fund_id
    )
    SELECT f.fund_name
    FROM funds AS f
    JOIN latest_nav AS ln
        ON f.fund_id = ln.fund_id
    """

    print(
        "CTE validation:",
        validate_finance_read_only_sql(valid_sql)
    )

    unauthorized_sql = """
    SELECT * FROM customers
    """

    try:
        validate_finance_read_only_sql(unauthorized_sql)
    except ValueError as error:
        print("Unauthorized table test: PASSED")
        print("Reason:", error)

    write_sql = """
    DELETE FROM funds
    """

    try:
        validate_finance_read_only_sql(write_sql)
    except ValueError:
        print("Read-only test: PASSED")
