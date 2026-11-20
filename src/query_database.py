from sqlalchemy import text
from src.database import engine


def run_query():
    queries = {
        "1. Customers and their order counts": """
            SELECT
                c.name,
                COUNT(o.order_id) AS order_count
            FROM customers AS c
            LEFT JOIN orders AS o
                ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY order_count DESC;
        """,

        "2. Total revenue by customer": """
            SELECT
                c.name,
                SUM(o.total) AS total_spent
            FROM customers AS c
            JOIN orders AS o
                ON c.customer_id = o.customer_id
            GROUP BY c.customer_id, c.name
            ORDER BY total_spent DESC;
        """,

        "3. Products with prices above 100": """
            SELECT
                name,
                price,
                category
            FROM products
            WHERE price > 100
            ORDER BY price DESC;
        """
    }

    with engine.connect() as connection:
        for title, query in queries.items():
            print(f"\n{title}")
            print("-" * 50)

            results = connection.execute(text(query))

            for row in results:
                print(row)


if __name__ == "__main__":
    run_query()