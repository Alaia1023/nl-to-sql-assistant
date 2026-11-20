import sqlglot
from sqlglot import exp


ALLOWED_TABLES = {
    "customers",
    "orders",
    "products",
    "order_items",
}


def validate_read_only_sql(sql):
    try:
        statements = sqlglot.parse(sql, read="sqlite")
    except sqlglot.errors.ParseError as error:
        raise ValueError("Invalid SQL syntax.") from error

    if len(statements) != 1 or statements[0] is None:
        raise ValueError("Only one SQL statement is allowed.")

    statement = statements[0]

    if not isinstance(statement, exp.Query):
        raise ValueError("Only read-only SELECT queries are allowed.")

    if isinstance(statement, exp.With):
        raise ValueError("Unexpected SQL statement type.")

    tables = {
        table.name
        for table in statement.find_all(exp.Table)
    }

    if not tables.issubset(ALLOWED_TABLES):
        raise ValueError("Query references an unauthorized table.")

    return True
