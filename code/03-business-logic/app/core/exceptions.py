"""
Custom Exceptions for Order Service
Lab 3 Complete: Business logic exceptions.
"""


class OrderServiceError(Exception):
    """Base exception for order service."""
    pass


class OrderNotFoundError(OrderServiceError):
    """Raised when order is not found."""
    def __init__(self, order_id: int):
        self.order_id = order_id
        super().__init__(f"Order with ID {order_id} not found")


class InvalidStatusTransitionError(OrderServiceError):
    """Raised when status transition is not allowed."""
    def __init__(self, current_status: str, new_status: str):
        self.current_status = current_status
        self.new_status = new_status
        super().__init__(
            f"Cannot transition from '{current_status}' to '{new_status}'"
        )


class OrderCancellationError(OrderServiceError):
    """Raised when order cannot be cancelled."""
    def __init__(self, order_id: int, status: str):
        self.order_id = order_id
        self.status = status
        super().__init__(
            f"Cannot cancel order {order_id} in '{status}' status"
        )


class ProductNotFoundError(OrderServiceError):
    """Raised when product is not found."""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class InsufficientStockError(OrderServiceError):
    """Raised when product stock is insufficient."""
    def __init__(self, product_id: int, product_name: str):
        self.product_id = product_id
        self.product_name = product_name
        super().__init__(f"Insufficient stock for product '{product_name}' (ID: {product_id})")
