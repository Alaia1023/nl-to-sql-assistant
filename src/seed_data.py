from datetime import date

from sqlalchemy.orm import Session

from src.database import Base, engine
from src.models import Customer, Order, Product, OrderItem


def seed_database():
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # Avoid inserting duplicate data
        if session.query(Customer).first():
            print("Database already contains data.")
            return

        customers = [
            Customer(name="Alice Johnson", email="alice@example.com"),
            Customer(name="Bob Smith", email="bob@example.com"),
            Customer(name="Charlie Brown", email="charlie@example.com"),
            Customer(name="Diana Wilson", email="diana@example.com"),
            Customer(name="Emma Davis", email="emma@example.com"),
        ]

        products = [
            Product(name="Laptop", price=1200.0, category="Electronics"),
            Product(name="Mouse", price=25.0, category="Electronics"),
            Product(name="Keyboard", price=75.0, category="Electronics"),
            Product(name="Desk", price=350.0, category="Furniture"),
            Product(name="Chair", price=200.0, category="Furniture"),
            Product(name="Notebook", price=5.0, category="Stationery"),
        ]

        session.add_all(customers)
        session.add_all(products)
        session.flush()

        orders = [
            Order(customer_id=customers[0].customer_id,
                  order_date=date(2026, 1, 10), total=1250.0),
            Order(customer_id=customers[0].customer_id,
                  order_date=date(2026, 1, 15), total=350.0),
            Order(customer_id=customers[0].customer_id,
                  order_date=date(2026, 2, 1), total=225.0),
            Order(customer_id=customers[0].customer_id,
                  order_date=date(2026, 2, 10), total=1200.0),
            Order(customer_id=customers[1].customer_id,
                  order_date=date(2026, 1, 12), total=200.0),
            Order(customer_id=customers[1].customer_id,
                  order_date=date(2026, 2, 5), total=75.0),
            Order(customer_id=customers[2].customer_id,
                  order_date=date(2026, 1, 20), total=350.0),
            Order(customer_id=customers[3].customer_id,
                  order_date=date(2026, 2, 12), total=25.0),
        ]

        session.add_all(orders)
        session.flush()

        order_items = [
            OrderItem(order_id=orders[0].order_id,
                      product_id=products[0].product_id, quantity=1),
            OrderItem(order_id=orders[0].order_id,
                      product_id=products[1].product_id, quantity=2),
            OrderItem(order_id=orders[1].order_id,
                      product_id=products[3].product_id, quantity=1),
            OrderItem(order_id=orders[2].order_id,
                      product_id=products[4].product_id, quantity=1),
            OrderItem(order_id=orders[3].order_id,
                      product_id=products[0].product_id, quantity=1),
            OrderItem(order_id=orders[4].order_id,
                      product_id=products[4].product_id, quantity=1),
            OrderItem(order_id=orders[5].order_id,
                      product_id=products[2].product_id, quantity=1),
            OrderItem(order_id=orders[6].order_id,
                      product_id=products[3].product_id, quantity=1),
            OrderItem(order_id=orders[7].order_id,
                      product_id=products[1].product_id, quantity=1),
        ]

        session.add_all(order_items)
        session.commit()

        print("Sample data inserted successfully!")
        print(f"Customers: {len(customers)}")
        print(f"Products: {len(products)}")
        print(f"Orders: {len(orders)}")
        print(f"Order items: {len(order_items)}")


if __name__ == "__main__":
    seed_database()
