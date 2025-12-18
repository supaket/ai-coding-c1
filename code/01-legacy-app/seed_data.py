"""
Seed Data Script - Run this to populate the database with sample data.
Usage: python seed_data.py
"""

from app import app, db, User, Product, Order, OrderItem
from decimal import Decimal

def seed_database():
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()
        
        # Create Users
        users = [
            User(email='alice@example.com', name='Alice Johnson'),
            User(email='bob@example.com', name='Bob Smith'),
            User(email='carol@example.com', name='Carol Williams'),
        ]
        db.session.add_all(users)
        db.session.commit()
        
        # Create Products
        products = [
            Product(name='Laptop Pro 15"', description='High-performance laptop', 
                    price=Decimal('1299.99'), stock=50, category='Electronics'),
            Product(name='Wireless Mouse', description='Ergonomic wireless mouse', 
                    price=Decimal('49.99'), stock=200, category='Electronics'),
            Product(name='USB-C Hub', description='7-in-1 USB-C hub', 
                    price=Decimal('79.99'), stock=150, category='Electronics'),
            Product(name='Mechanical Keyboard', description='RGB mechanical keyboard', 
                    price=Decimal('149.99'), stock=100, category='Electronics'),
            Product(name='Monitor 27"', description='4K IPS monitor', 
                    price=Decimal('449.99'), stock=30, category='Electronics'),
            Product(name='Desk Lamp', description='LED desk lamp with dimmer', 
                    price=Decimal('39.99'), stock=80, category='Office'),
            Product(name='Office Chair', description='Ergonomic office chair', 
                    price=Decimal('299.99'), stock=25, category='Furniture'),
            Product(name='Standing Desk', description='Electric standing desk', 
                    price=Decimal('599.99'), stock=15, category='Furniture'),
        ]
        db.session.add_all(products)
        db.session.commit()
        
        # Create Sample Orders
        # Order 1: Alice - Pending
        order1 = Order(user_id=1, status='pending', 
                       shipping_address='123 Main St, City, ST 12345')
        order1.items.append(OrderItem(product_id=1, product_name='Laptop Pro 15"', 
                                       quantity=1, unit_price=Decimal('1299.99')))
        order1.items.append(OrderItem(product_id=2, product_name='Wireless Mouse', 
                                       quantity=2, unit_price=Decimal('49.99')))
        order1.total = Decimal('1399.97')
        
        # Order 2: Alice - Delivered
        order2 = Order(user_id=1, status='delivered', 
                       shipping_address='123 Main St, City, ST 12345')
        order2.items.append(OrderItem(product_id=4, product_name='Mechanical Keyboard', 
                                       quantity=1, unit_price=Decimal('149.99')))
        order2.total = Decimal('149.99')
        
        # Order 3: Bob - Processing
        order3 = Order(user_id=2, status='processing', 
                       shipping_address='456 Oak Ave, Town, ST 67890')
        order3.items.append(OrderItem(product_id=5, product_name='Monitor 27"', 
                                       quantity=2, unit_price=Decimal('449.99')))
        order3.items.append(OrderItem(product_id=3, product_name='USB-C Hub', 
                                       quantity=1, unit_price=Decimal('79.99')))
        order3.total = Decimal('979.97')
        
        # Order 4: Carol - Shipped
        order4 = Order(user_id=3, status='shipped', 
                       shipping_address='789 Pine Rd, Village, ST 11111')
        order4.items.append(OrderItem(product_id=7, product_name='Office Chair', 
                                       quantity=1, unit_price=Decimal('299.99')))
        order4.items.append(OrderItem(product_id=6, product_name='Desk Lamp', 
                                       quantity=2, unit_price=Decimal('39.99')))
        order4.total = Decimal('379.97')
        
        db.session.add_all([order1, order2, order3, order4])
        db.session.commit()
        
        print("✅ Database seeded successfully!")
        print(f"   - {len(users)} users")
        print(f"   - {len(products)} products")
        print(f"   - 4 orders")
        print("\n🚀 Run 'python app.py' to start the server")
        print("📖 API: http://localhost:5000/api/orders")


if __name__ == '__main__':
    seed_database()
