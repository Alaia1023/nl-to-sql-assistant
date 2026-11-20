DATABASE_SCHEMA = """
Database: Online Shop

Table: customers
- customer_id: INTEGER, primary key
- name: TEXT
- email: TEXT

Table: orders
- order_id: INTEGER, primary key
- customer_id: INTEGER, foreign key referencing customers.customer_id
- order_date: DATE
- total: REAL

Table: products
- product_id: INTEGER, primary key
- name: TEXT
- price: REAL
- category: TEXT

Table: order_items
- item_id: INTEGER, primary key
- order_id: INTEGER, foreign key referencing orders.order_id
- product_id: INTEGER, foreign key referencing products.product_id
- quantity: INTEGER

Relationships:
- One customer can have many orders.
- One order can have many order items.
- One product can appear in many order items.
"""
