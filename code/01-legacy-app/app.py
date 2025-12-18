"""
ShopFast Legacy Monolith - Flask Application
=============================================
This is the legacy application students will analyze in Lab 1.

Run: python app.py
Seed: python seed_data.py
Test: http://localhost:5000/api/orders
"""

from datetime import datetime
from decimal import Decimal
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopfast.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# ==================== MODELS ====================

class User(db.Model):
    """User model - handles authentication and profiles."""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }


class Product(db.Model):
    """Product catalog model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, default=0)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'stock': self.stock,
            'category': self.category
        }


class Order(db.Model):
    """Order model - THIS IS WHAT WE'LL EXTRACT."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    total = db.Column(db.Numeric(10, 2), default=0)
    shipping_address = db.Column(db.String(500))
    notes = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

    # Valid status transitions
    VALID_TRANSITIONS = {
        'pending': ['confirmed', 'cancelled'],
        'confirmed': ['processing', 'cancelled'],
        'processing': ['shipped', 'cancelled'],
        'shipped': ['delivered'],
        'delivered': [],
        'cancelled': []
    }

    def can_transition_to(self, new_status):
        return new_status in self.VALID_TRANSITIONS.get(self.status, [])

    def to_dict(self, include_items=True):
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'total': float(self.total),
            'shipping_address': self.shipping_address,
            'notes': self.notes,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
            data['item_count'] = len(self.items)
        return data


class OrderItem(db.Model):
    """Order line items."""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

    @property
    def subtotal(self):
        return self.quantity * self.unit_price

    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal)
        }


# ==================== USER ENDPOINTS ====================

@app.route('/api/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(email=data['email'], name=data['name'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


# ==================== PRODUCT ENDPOINTS ====================

@app.route('/api/products', methods=['GET'])
def list_products():
    category = request.args.get('category')
    query = Product.query
    if category:
        query = query.filter_by(category=category)
    products = query.all()
    return jsonify([p.to_dict() for p in products])


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict())


@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=Decimal(str(data['price'])),
        stock=data.get('stock', 0),
        category=data.get('category')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


# ==================== ORDER ENDPOINTS (TARGET FOR EXTRACTION) ====================

@app.route('/api/orders', methods=['GET'])
def list_orders():
    """List orders with optional filtering."""
    user_id = request.args.get('user_id', type=int)
    status = request.args.get('status')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Order.query
    if user_id:
        query = query.filter_by(user_id=user_id)
    if status:
        query = query.filter_by(status=status)
    
    pagination = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [o.to_dict(include_items=False) for o in pagination.items],
        'total': pagination.total,
        'page': page,
        'per_page': per_page,
        'pages': pagination.pages
    })


@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details with items."""
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())


@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order with items."""
    data = request.json
    
    # Validate user exists
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Create order
    order = Order(
        user_id=data['user_id'],
        shipping_address=data.get('shipping_address'),
        notes=data.get('notes')
    )
    
    # Add items and calculate total
    total = Decimal('0.00')
    for item_data in data.get('items', []):
        product = Product.query.get(item_data['product_id'])
        if not product:
            return jsonify({'error': f"Product {item_data['product_id']} not found"}), 404
        
        if product.stock < item_data['quantity']:
            return jsonify({'error': f"Insufficient stock for {product.name}"}), 400
        
        item = OrderItem(
            product_id=product.id,
            product_name=product.name,
            quantity=item_data['quantity'],
            unit_price=product.price
        )
        order.items.append(item)
        total += item.subtotal
        
        # Reduce stock
        product.stock -= item_data['quantity']
    
    order.total = total
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_dict()), 201


@app.route('/api/orders/<int:order_id>', methods=['PATCH'])
def update_order(order_id):
    """Update order status."""
    order = Order.query.get_or_404(order_id)
    data = request.json
    
    if 'status' in data:
        new_status = data['status']
        if not order.can_transition_to(new_status):
            return jsonify({
                'error': f"Cannot transition from '{order.status}' to '{new_status}'",
                'valid_transitions': Order.VALID_TRANSITIONS[order.status]
            }), 400
        order.status = new_status
    
    if 'shipping_address' in data:
        order.shipping_address = data['shipping_address']
    
    if 'notes' in data:
        order.notes = data['notes']
    
    db.session.commit()
    return jsonify(order.to_dict())


@app.route('/api/orders/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order and restore stock."""
    order = Order.query.get_or_404(order_id)
    
    if not order.can_transition_to('cancelled'):
        return jsonify({
            'error': f"Cannot cancel order in '{order.status}' status"
        }), 400
    
    # Restore stock
    for item in order.items:
        product = Product.query.get(item.product_id)
        if product:
            product.stock += item.quantity
    
    order.status = 'cancelled'
    db.session.commit()
    
    return jsonify(order.to_dict())


@app.route('/api/users/<int:user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    """Get all orders for a specific user."""
    User.query.get_or_404(user_id)  # Verify user exists
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])


# ==================== HEALTH CHECK ====================

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'service': 'shopfast-monolith'})


# ==================== MAIN ====================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
