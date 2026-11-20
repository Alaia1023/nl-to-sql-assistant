from src.schema import DATABASE_SCHEMA
from src.business_knowledge import format_business_knowledge

SYSTEM_INSTRUCTION = """
You are an expert Text-to-SQL assistant.
Convert the user's question into exactly one valid SQLite SELECT query.
Return SQL only. Do not include explanations or Markdown.
Never modify the database.
"""


DETAILED_SCHEMA = """
Database tables and relationships:

1. customers
   - customer_id: INTEGER, primary key
   - name: TEXT
   - email: TEXT, unique

2. orders
   - order_id: INTEGER, primary key
   - customer_id: INTEGER, foreign key to customers.customer_id
   - order_date: DATE
   - total: REAL
   - Each order belongs to one customer.

3. products
   - product_id: INTEGER, primary key
   - name: TEXT
   - price: REAL
   - category: TEXT

4. order_items
   - item_id: INTEGER, primary key
   - order_id: INTEGER, foreign key to orders.order_id
   - product_id: INTEGER, foreign key to products.product_id
   - quantity: INTEGER
   - Each order item belongs to one order and one product.

Use JOIN conditions based on the foreign keys.
Use SQLite-compatible SQL syntax.
"""


FEW_SHOT_EXAMPLES = """
Example 1

Question:
List all customer names.

SQL:
SELECT name
FROM customers;

Example 2

Question:
How many orders does each customer have?

SQL:
SELECT c.name, COUNT(o.order_id) AS order_count
FROM customers AS c
LEFT JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY c.customer_id;

Example 3

Question:
What is the total amount spent by each customer?

SQL:
SELECT c.name, SUM(o.total) AS total_spent
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_spent DESC;
"""


def build_prompt(question, strategy):
    if strategy == "S0":
        schema = DATABASE_SCHEMA
        extra = ""

    elif strategy == "S1":
        schema = DETAILED_SCHEMA
        extra = """
Pay close attention to primary keys, foreign keys,
table relationships, and the correct use of JOIN and GROUP BY.
"""

    elif strategy == "S2":
        schema = DETAILED_SCHEMA
        extra = FEW_SHOT_EXAMPLES

    elif strategy == "S3":
        schema = DETAILED_SCHEMA
        business_knowledge = format_business_knowledge()

        extra = f"""
{FEW_SHOT_EXAMPLES}

Business Knowledge Base:
{business_knowledge}

Business knowledge instructions:
- Use business definitions to interpret the user's terminology.
- Use the specified business calculations when relevant.
- Do not generalize a rule beyond the situation it describes.
- Choose INNER JOIN when only entities with matching related records
  should contribute to the result.
- Choose LEFT JOIN only when the question requires retaining entities
  even when they have no matching related records.
- Do not use LEFT JOIN automatically for every product aggregation.
- Use COALESCE only when missing aggregate values should be displayed as zero.
- Use WHERE for row-level filtering and HAVING for aggregate filtering.

Output column instructions:
- Select columns that directly answer the user's question.
- Include the relevant numeric value when the question asks about a price,
  count, quantity, revenue, or total amount.
- Do not omit a requested measure from the SELECT clause.
- Do not add unrelated identifiers or columns.
- Include identifying information for the entities being returned.
- Use GROUP BY for non-aggregated selected columns when aggregation is used.
- Add ORDER BY only when requested or when the question clearly implies
  a ranking such as highest, lowest, most, or least.
- Do not change the meaning of the question to satisfy a business rule.
"""

    else:
        raise ValueError(f"Unknown prompt strategy: {strategy}")

    return f"""
{SYSTEM_INSTRUCTION}

Database schema:
{schema}

{extra}

User question:
{question}

Return exactly one SQLite SELECT query.
"""
