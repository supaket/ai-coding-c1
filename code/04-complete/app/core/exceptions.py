"""
Custom Exceptions for ShopFast API
Full API: Business logic exceptions for all services.
"""


class ShopFastError(Exception):
    """Base exception for ShopFast API."""
    pass


# Order Exceptions
class OrderServiceError(ShopFastError):
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


# User Exceptions
class UserServiceError(ShopFastError):
    """Base exception for user service."""
    pass


class UserNotFoundError(UserServiceError):
    """Raised when user is not found."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User with ID {user_id} not found")


class UserAlreadyExistsError(UserServiceError):
    """Raised when user email already exists."""
    def __init__(self, email: str):
        self.email = email
        super().__init__(f"User with email '{email}' already exists")


# Product Exceptions
class ProductServiceError(ShopFastError):
    """Base exception for product service."""
    pass


class ProductNotFoundError(ProductServiceError):
    """Raised when product is not found."""
    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class InsufficientStockError(ProductServiceError):
    """Raised when product has insufficient stock."""
    def __init__(self, product_id: int, requested: int, available: int):
        self.product_id = product_id
        self.requested = requested
        self.available = available
        super().__init__(
            f"Insufficient stock for product {product_id}: "
            f"requested {requested}, available {available}"
        )


# Notification Exceptions
class NotificationServiceError(ShopFastError):
    """Base exception for notification service."""
    pass


class NotificationNotFoundError(NotificationServiceError):
    """Raised when notification is not found."""
    def __init__(self, notification_id: int):
        self.notification_id = notification_id
        super().__init__(f"Notification with ID {notification_id} not found")
