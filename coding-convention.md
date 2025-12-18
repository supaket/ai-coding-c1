# Python Coding Convention 2025

## Professional Standards for Modern Python Development

**Version:** 1.0  
**Last Updated:** December 2025  
**Applies to:** Python 3.11+

---

## Table of Contents

1. [Philosophy & Principles](#philosophy--principles)
2. [Code Layout & Formatting](#code-layout--formatting)
3. [Naming Conventions](#naming-conventions)
4. [Type Hints & Annotations](#type-hints--annotations)
5. [Documentation](#documentation)
6. [Imports](#imports)
7. [Functions & Methods](#functions--methods)
8. [Classes & Object-Oriented Design](#classes--object-oriented-design)
9. [Error Handling](#error-handling)
10. [Async & Concurrency](#async--concurrency)
11. [Testing Standards](#testing-standards)
12. [Security Practices](#security-practices)
13. [Performance Guidelines](#performance-guidelines)
14. [Project Structure](#project-structure)
15. [Tooling & Automation](#tooling--automation)

---

## Philosophy & Principles

### The Zen of Professional Python

```
Readability is non-negotiable.
Explicit intent beats clever tricks.
Type safety prevents runtime surprises.
Tests are documentation that executes.
Security is a feature, not an afterthought.
```

### Core Principles

**Readability First** — Code is read 10x more than written. Optimize for the reader, including your future self.

**Progressive Type Safety** — Embrace Python's type system. Every function signature should be typed. Every data structure should be annotated.

**Fail Fast, Fail Loud** — Errors should surface immediately with clear context. Silent failures are bugs waiting to happen.

**Immutability by Default** — Prefer immutable data structures. Mutation should be intentional and localized.

**Composition Over Inheritance** — Build systems from small, focused components. Deep inheritance hierarchies obscure behavior.

---

## Code Layout & Formatting

### Line Length

```python
# Maximum line length: 88 characters (Black default)
# Documentation strings: 72 characters
# Comments: 72 characters
```

### Indentation

Use 4 spaces. Never tabs.

```python
# Correct
def calculate_total(
    items: list[Item],
    discount: Decimal,
    tax_rate: Decimal,
) -> Decimal:
    subtotal = sum(item.price for item in items)
    discounted = subtotal * (1 - discount)
    return discounted * (1 + tax_rate)
```

### Blank Lines

```python
# Two blank lines before top-level definitions
import os


class UserService:
    """Handles user-related operations."""

    # One blank line between methods
    def create_user(self, data: UserCreate) -> User:
        ...

    def delete_user(self, user_id: UUID) -> None:
        ...


def standalone_function() -> None:
    ...
```

### Trailing Commas

Always use trailing commas in multi-line structures:

```python
# Correct — enables cleaner diffs
config = {
    "host": "localhost",
    "port": 5432,
    "database": "app_db",
}

# Correct — function arguments
result = complex_function(
    first_argument,
    second_argument,
    third_argument,
)
```

### String Quotes

Use double quotes for strings. Single quotes only when the string contains double quotes.

```python
# Correct
message = "Hello, world"
html = '<div class="container">Content</div>'

# Incorrect
message = 'Hello, world'
```

---

## Naming Conventions

### Summary Table

| Type | Convention | Example |
|------|------------|---------|
| Module | snake_case | `user_service.py` |
| Package | snake_case | `data_processing` |
| Class | PascalCase | `UserRepository` |
| Function | snake_case | `calculate_total` |
| Method | snake_case | `get_user_by_id` |
| Variable | snake_case | `user_count` |
| Constant | SCREAMING_SNAKE | `MAX_RETRIES` |
| Type Variable | PascalCase | `T`, `UserT` |
| Protocol | PascalCase + able/ible | `Serializable` |
| Private | _leading_underscore | `_internal_cache` |
| "Dunder" | __double_underscore__ | `__init__` |

### Naming Guidelines

**Be Descriptive, Not Verbose**

```python
# Good — clear and concise
def get_active_users() -> list[User]:
    ...

user_ids: set[UUID] = set()

# Bad — too abbreviated
def get_act_usrs():
    ...

uids: set = set()

# Bad — unnecessarily verbose
def get_all_currently_active_user_objects_from_database():
    ...
```

**Boolean Names**

Prefix with `is_`, `has_`, `can_`, `should_`, or `allows_`:

```python
is_active: bool = True
has_permission: bool = user.check_permission(resource)
can_edit: bool = role in EDITOR_ROLES
should_retry: bool = attempt < MAX_RETRIES
allows_anonymous: bool = endpoint.public
```

**Collection Names**

Use plural nouns:

```python
users: list[User] = []
user_ids: set[UUID] = set()
email_to_user: dict[str, User] = {}
```

**Function Names**

Use verb phrases that describe the action:

```python
def create_user(data: UserCreate) -> User: ...
def validate_email(email: str) -> bool: ...
def send_notification(user: User, message: str) -> None: ...
def calculate_discount(order: Order) -> Decimal: ...
```

### Avoid These Anti-Patterns

```python
# Avoid single-letter names (except in comprehensions/lambdas)
# Bad
x = get_user()
d = load_data()

# Good
user = get_user()
dataset = load_data()

# Avoid type prefixes (Hungarian notation)
# Bad
str_name = "John"
lst_users = []
dict_config = {}

# Good
name = "John"
users = []
config = {}

# Avoid abbreviations that aren't universally understood
# Bad
usr_mgr = UserManager()
cfg = load_config()

# Good
user_manager = UserManager()
config = load_config()
```

---

## Type Hints & Annotations

### Required Type Hints

Every function must have complete type annotations:

```python
from collections.abc import Callable, Iterable, Mapping
from typing import Any, TypeVar, ParamSpec

T = TypeVar("T")
P = ParamSpec("P")


def process_items(
    items: Iterable[T],
    transformer: Callable[[T], T],
    *,
    filter_fn: Callable[[T], bool] | None = None,
) -> list[T]:
    """Process items with transformation and optional filtering."""
    if filter_fn:
        items = (item for item in items if filter_fn(item))
    return [transformer(item) for item in items]
```

### Modern Type Hint Syntax (Python 3.10+)

```python
# Use built-in generics (not typing module)
# Good
def get_users() -> list[User]: ...
def get_config() -> dict[str, Any]: ...
def find_user(user_id: int) -> User | None: ...

# Avoid (legacy style)
from typing import List, Dict, Optional
def get_users() -> List[User]: ...
def get_config() -> Dict[str, Any]: ...
def find_user(user_id: int) -> Optional[User]: ...
```

### TypedDict for Structured Data

```python
from typing import TypedDict, NotRequired


class UserCreate(TypedDict):
    email: str
    name: str
    password: str
    phone: NotRequired[str]


class UserResponse(TypedDict):
    id: int
    email: str
    name: str
    created_at: str
```

### Protocols for Structural Typing

```python
from typing import Protocol, runtime_checkable


@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict[str, Any]: ...
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Serializable": ...


class Cacheable(Protocol):
    @property
    def cache_key(self) -> str: ...
    
    @property
    def cache_ttl(self) -> int: ...
```

### NewType for Type Safety

```python
from typing import NewType

UserId = NewType("UserId", int)
OrderId = NewType("OrderId", int)
Email = NewType("Email", str)


def get_user(user_id: UserId) -> User: ...
def get_order(order_id: OrderId) -> Order: ...

# Type checker will catch this error:
# get_user(OrderId(123))  # Error: Expected UserId, got OrderId
```

### Dataclasses and Attrs

Prefer dataclasses or attrs over plain classes for data containers:

```python
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class User:
    """Immutable user entity."""
    
    id: UUID = field(default_factory=uuid4)
    email: str
    name: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    roles: frozenset[str] = field(default_factory=frozenset)


@dataclass(slots=True)
class UserUpdate:
    """Mutable DTO for user updates."""
    
    name: str | None = None
    email: str | None = None
```

---

## Documentation

### Docstring Format (Google Style)

```python
def calculate_shipping_cost(
    items: list[Item],
    destination: Address,
    *,
    express: bool = False,
    insurance: bool = False,
) -> ShippingQuote:
    """Calculate shipping cost for a list of items to a destination.

    Computes the optimal shipping rate based on item dimensions, weight,
    and destination. Supports express delivery and optional insurance.

    Args:
        items: List of items to be shipped. Each item must have weight
            and dimensions defined.
        destination: Delivery address including country code for
            international rate calculation.
        express: If True, calculate express delivery rates (2-3 days).
            Defaults to standard shipping (5-7 days).
        insurance: If True, include shipping insurance in the quote.
            Insurance cost is 2% of declared item value.

    Returns:
        ShippingQuote containing carrier options, estimated delivery
        dates, and itemized costs.

    Raises:
        ShippingUnavailableError: If no carriers service the destination.
        InvalidItemError: If any item exceeds maximum shipping dimensions.
        AddressValidationError: If the destination address is incomplete.

    Example:
        >>> items = [Item(weight=2.5, length=30, width=20, height=10)]
        >>> address = Address(country="US", zip_code="90210")
        >>> quote = calculate_shipping_cost(items, address, express=True)
        >>> print(f"Express shipping: ${quote.total:.2f}")
        Express shipping: $24.99

    Note:
        Rates are cached for 1 hour. For real-time rates, use
        `calculate_shipping_cost_realtime()`.
    """
    ...
```

### Module Docstrings

```python
"""User authentication and authorization module.

This module provides comprehensive authentication services including:

- Password-based authentication with bcrypt hashing
- JWT token generation and validation
- OAuth2 integration (Google, GitHub, Microsoft)
- Role-based access control (RBAC)
- Session management with Redis backend

Typical usage:

    from auth import AuthService, TokenConfig

    auth = AuthService(TokenConfig(secret_key="..."))
    
    # Authenticate user
    user = await auth.authenticate("user@example.com", "password")
    
    # Generate access token
    token = auth.create_access_token(user)

Configuration is loaded from environment variables. See `auth.config`
for available options.

Attributes:
    DEFAULT_TOKEN_EXPIRY: Default JWT expiration time (1 hour).
    MAX_LOGIN_ATTEMPTS: Maximum failed attempts before lockout (5).

Todo:
    * Add support for WebAuthn/FIDO2
    * Implement refresh token rotation
"""

from __future__ import annotations
...
```

### Class Docstrings

```python
class OrderProcessor:
    """Processes customer orders through the fulfillment pipeline.

    Manages the complete order lifecycle from validation through
    shipping notification. Integrates with inventory, payment,
    and shipping services.

    The processor is designed for high throughput and supports
    concurrent processing of multiple orders.

    Attributes:
        inventory: Inventory service for stock verification.
        payment: Payment gateway for transaction processing.
        shipping: Shipping service for label generation.
        max_concurrent: Maximum concurrent orders to process.

    Example:
        >>> processor = OrderProcessor(
        ...     inventory=InventoryService(),
        ...     payment=PaymentGateway(),
        ...     shipping=ShippingService(),
        ... )
        >>> result = await processor.process(order)
        >>> print(f"Order {result.order_id} processed: {result.status}")
    """

    def __init__(
        self,
        inventory: InventoryService,
        payment: PaymentGateway,
        shipping: ShippingService,
        *,
        max_concurrent: int = 10,
    ) -> None:
        """Initialize the order processor.

        Args:
            inventory: Service for checking and reserving stock.
            payment: Gateway for processing payments.
            shipping: Service for shipping label generation.
            max_concurrent: Maximum orders to process concurrently.
                Defaults to 10.
        """
        ...
```

### Inline Comments

```python
# Use comments to explain WHY, not WHAT
# The code shows what; comments explain reasoning

# Bad — states the obvious
user_count = len(users)  # Get the count of users

# Good — explains the reasoning
# Cache user count to avoid repeated database queries during pagination
user_count = await cache.get_or_set("user_count", fetch_user_count, ttl=300)

# Good — documents a non-obvious decision
# Using insertion order dict (Python 3.7+) to maintain priority sequence
priority_handlers: dict[str, Handler] = {}

# Good — warns about potential issues
# CAUTION: This operation is not thread-safe. Use lock in concurrent context.
self._cache.clear()
```

---

## Imports

### Import Order

```python
"""Module docstring."""

# 1. Future imports (if needed for compatibility)
from __future__ import annotations

# 2. Standard library imports
import asyncio
import logging
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, TypeVar
from uuid import UUID

# 3. Third-party imports
import httpx
from pydantic import BaseModel, Field
from sqlalchemy import Column, String
from sqlalchemy.orm import Session

# 4. Local application imports
from app.core.config import settings
from app.models.user import User
from app.services.email import EmailService

# 5. Relative imports (within the same package)
from .exceptions import ValidationError
from .types import UserId
```

### Import Guidelines

```python
# Prefer explicit imports over wildcards
# Good
from typing import Any, TypeVar, Protocol

# Bad — never use wildcard imports
from typing import *

# Import modules, not just classes, when it improves clarity
# Good — clear namespace
from datetime import datetime
from decimal import Decimal

# Also acceptable — when module is small/focused
import datetime
import decimal

# For common libraries, use conventional aliases
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
import torch

# Avoid deep relative imports
# Bad
from ...utils.helpers.strings import slugify

# Good — use absolute imports
from app.utils.helpers.strings import slugify
```

### Managing Circular Imports

```python
# Use TYPE_CHECKING for type-only imports
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.order import Order
    from app.services.payment import PaymentService


class OrderProcessor:
    def __init__(self, payment_service: "PaymentService") -> None:
        self.payment = payment_service

    def process(self, order: "Order") -> None:
        ...
```

---

## Functions & Methods

### Function Design Principles

**Single Responsibility** — Each function should do one thing well.

```python
# Bad — does too many things
def process_user_registration(data: dict) -> User:
    # Validates input
    # Checks for duplicates
    # Hashes password
    # Creates user
    # Sends welcome email
    # Logs analytics
    ...

# Good — single responsibility, composed
async def register_user(data: UserCreate) -> User:
    """Register a new user account."""
    validated = validate_registration(data)
    await check_email_available(validated.email)
    user = await create_user(validated)
    await send_welcome_email(user)
    return user
```

**Pure Functions When Possible**

```python
# Pure function — same input always gives same output, no side effects
def calculate_tax(amount: Decimal, rate: Decimal) -> Decimal:
    return amount * rate


# Impure but clearly marked
async def fetch_user(user_id: UserId) -> User:
    """Fetch user from database (I/O operation)."""
    ...
```

### Parameter Guidelines

```python
# Maximum 5-6 positional parameters; use dataclass/TypedDict for more
# Bad
def create_order(
    user_id, product_id, quantity, price, discount, 
    tax_rate, shipping_address, billing_address, 
    payment_method, notes, priority
):
    ...

# Good — group related parameters
@dataclass
class OrderRequest:
    user_id: UserId
    items: list[OrderItem]
    shipping_address: Address
    billing_address: Address
    payment_method: PaymentMethod
    notes: str = ""
    priority: OrderPriority = OrderPriority.STANDARD


def create_order(request: OrderRequest) -> Order:
    ...
```

**Use Keyword-Only Arguments**

```python
# Force keyword usage for clarity
def connect(
    host: str,
    port: int,
    *,  # Everything after is keyword-only
    timeout: float = 30.0,
    retries: int = 3,
    ssl: bool = True,
) -> Connection:
    ...

# Usage is explicit and readable
conn = connect("db.example.com", 5432, timeout=60.0, ssl=True)
```

**Avoid Mutable Default Arguments**

```python
# Bad — mutable default is shared across calls
def add_item(item: str, items: list[str] = []) -> list[str]:
    items.append(item)
    return items

# Good — use None and create new instance
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

# Better — use field factory for dataclasses
@dataclass
class Container:
    items: list[str] = field(default_factory=list)
```

### Return Values

```python
# Be explicit about None returns
def find_user(email: str) -> User | None:
    """Find user by email, returns None if not found."""
    ...

# Use sentinel values or exceptions for "not found" when None is a valid value
class NotFound:
    """Sentinel for missing values when None is valid."""
    _instance = None
    
    def __new__(cls) -> "NotFound":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


NOT_FOUND = NotFound()


def get_config_value(key: str) -> str | None | NotFound:
    """Get config value. Returns NOT_FOUND if key doesn't exist."""
    ...
```

---

## Classes & Object-Oriented Design

### Class Design Principles

```python
from abc import ABC, abstractmethod
from typing import Protocol


# Prefer composition over inheritance
class EmailNotifier:
    def __init__(self, email_service: EmailService) -> None:
        self._email = email_service

    def notify(self, user: User, message: str) -> None:
        self._email.send(user.email, message)


class SMSNotifier:
    def __init__(self, sms_service: SMSService) -> None:
        self._sms = sms_service

    def notify(self, user: User, message: str) -> None:
        self._sms.send(user.phone, message)


# Use protocols for interfaces
class Notifier(Protocol):
    def notify(self, user: User, message: str) -> None: ...


class NotificationService:
    def __init__(self, notifiers: list[Notifier]) -> None:
        self._notifiers = notifiers

    def send_all(self, user: User, message: str) -> None:
        for notifier in self._notifiers:
            notifier.notify(user, message)
```

### Property Usage

```python
@dataclass
class Rectangle:
    width: float
    height: float

    @property
    def area(self) -> float:
        """Calculate area (computed property)."""
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        """Calculate perimeter (computed property)."""
        return 2 * (self.width + self.height)


class User:
    def __init__(self, first_name: str, last_name: str) -> None:
        self._first_name = first_name
        self._last_name = last_name

    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"

    @full_name.setter
    def full_name(self, value: str) -> None:
        parts = value.split(" ", 1)
        self._first_name = parts[0]
        self._last_name = parts[1] if len(parts) > 1 else ""
```

### Dunder Methods

```python
from functools import total_ordering


@total_ordering
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def __repr__(self) -> str:
        return f"Version({self.major}, {self.minor}, {self.patch})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) == (
            other.major, other.minor, other.patch
        )

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Version):
            return NotImplemented
        return (self.major, self.minor, self.patch) < (
            other.major, other.minor, other.patch
        )

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch))
```

### Context Managers

```python
from contextlib import contextmanager, asynccontextmanager
from typing import Generator, AsyncGenerator


@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """Context manager that logs execution time."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} completed in {elapsed:.3f}s")


@asynccontextmanager
async def database_transaction(
    session: AsyncSession,
) -> AsyncGenerator[AsyncSession, None]:
    """Manage database transaction with automatic rollback on error."""
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise


# Class-based for complex state management
class ManagedResource:
    def __init__(self, config: ResourceConfig) -> None:
        self.config = config
        self._resource: Resource | None = None

    def __enter__(self) -> Resource:
        self._resource = acquire_resource(self.config)
        return self._resource

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        if self._resource:
            release_resource(self._resource)
        return False  # Don't suppress exceptions
```

---

## Error Handling

### Exception Hierarchy

```python
"""Application exception hierarchy."""


class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}


class ValidationError(AppError):
    """Input validation failed."""
    pass


class NotFoundError(AppError):
    """Requested resource not found."""
    pass


class ConflictError(AppError):
    """Operation conflicts with current state."""
    pass


class AuthenticationError(AppError):
    """Authentication failed."""
    pass


class AuthorizationError(AppError):
    """User lacks required permissions."""
    pass


class ExternalServiceError(AppError):
    """External service call failed."""

    def __init__(
        self,
        message: str,
        *,
        service: str,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(message, **kwargs)
        self.service = service
        self.status_code = status_code
```

### Exception Handling Best Practices

```python
# Be specific about exceptions
# Bad
try:
    result = process_data(data)
except Exception:
    logger.error("Something went wrong")

# Good
try:
    result = process_data(data)
except ValidationError as e:
    logger.warning(f"Invalid data: {e.message}", extra={"details": e.details})
    raise
except ExternalServiceError as e:
    logger.error(f"Service {e.service} failed: {e.message}")
    raise
except Exception as e:
    logger.exception("Unexpected error during data processing")
    raise AppError("Processing failed") from e


# Use context managers for cleanup
# Bad
file = open("data.txt")
try:
    data = file.read()
finally:
    file.close()

# Good
with open("data.txt") as file:
    data = file.read()


# Preserve exception context
try:
    external_api.call()
except HTTPError as e:
    # 'from e' preserves the original exception chain
    raise ExternalServiceError(
        "API call failed",
        service="external_api",
        status_code=e.response.status_code,
    ) from e
```

### Result Pattern (for Recoverable Errors)

```python
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


@dataclass(frozen=True)
class Ok(Generic[T]):
    value: T
    
    def is_ok(self) -> bool:
        return True
    
    def is_err(self) -> bool:
        return False


@dataclass(frozen=True)
class Err(Generic[E]):
    error: E
    
    def is_ok(self) -> bool:
        return False
    
    def is_err(self) -> bool:
        return True


Result = Ok[T] | Err[E]


def parse_config(path: Path) -> Result[Config, ConfigError]:
    """Parse configuration file, returning Result instead of raising."""
    try:
        content = path.read_text()
        data = json.loads(content)
        return Ok(Config(**data))
    except FileNotFoundError:
        return Err(ConfigError(f"Config file not found: {path}"))
    except json.JSONDecodeError as e:
        return Err(ConfigError(f"Invalid JSON: {e}"))
    except ValidationError as e:
        return Err(ConfigError(f"Invalid config: {e}"))


# Usage
match parse_config(Path("config.json")):
    case Ok(config):
        app.configure(config)
    case Err(error):
        logger.error(f"Configuration failed: {error}")
        sys.exit(1)
```

---

## Async & Concurrency

### Async Best Practices

```python
import asyncio
from collections.abc import Coroutine
from typing import Any


# Always use async/await, never blocking calls in async context
# Bad — blocks the event loop
async def fetch_data_bad(url: str) -> dict:
    response = requests.get(url)  # Blocking!
    return response.json()

# Good — non-blocking
async def fetch_data(url: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()


# Use asyncio.gather for concurrent operations
async def fetch_all_users(user_ids: list[int]) -> list[User]:
    tasks = [fetch_user(uid) for uid in user_ids]
    return await asyncio.gather(*tasks)


# Use asyncio.TaskGroup (Python 3.11+) for structured concurrency
async def process_batch(items: list[Item]) -> list[Result]:
    results: list[Result] = []
    
    async with asyncio.TaskGroup() as tg:
        for item in items:
            tg.create_task(process_item(item, results))
    
    return results


# Handle timeouts properly
async def fetch_with_timeout(url: str, timeout: float = 30.0) -> dict:
    try:
        async with asyncio.timeout(timeout):
            return await fetch_data(url)
    except TimeoutError:
        raise ExternalServiceError(
            f"Request timed out after {timeout}s",
            service=url,
        )
```

### Async Context Managers and Iterators

```python
from collections.abc import AsyncIterator


class AsyncDatabasePool:
    async def __aenter__(self) -> "AsyncDatabasePool":
        await self._connect()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._disconnect()


async def stream_records(query: str) -> AsyncIterator[Record]:
    """Stream database records without loading all into memory."""
    async with get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(query)
            async for row in cursor:
                yield Record.from_row(row)


# Usage
async for record in stream_records("SELECT * FROM large_table"):
    await process_record(record)
```

### Thread Safety

```python
import threading
from functools import lru_cache


# Use locks for shared mutable state
class ThreadSafeCounter:
    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value


# Use thread-local storage when appropriate
_local = threading.local()


def get_request_context() -> RequestContext:
    ctx = getattr(_local, "context", None)
    if ctx is None:
        raise RuntimeError("No request context available")
    return ctx


# Be careful with async and threads
async def run_blocking_in_thread(func: Callable[[], T]) -> T:
    """Run blocking function in thread pool."""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)
```

---

## Testing Standards

### Test Organization

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── unit/                    # Fast, isolated tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services.py
├── integration/             # Tests with real dependencies
│   ├── __init__.py
│   ├── test_api.py
│   └── test_database.py
└── e2e/                     # End-to-end tests
    ├── __init__.py
    └── test_workflows.py
```

### Test Writing Guidelines

```python
import pytest
from unittest.mock import AsyncMock, Mock, patch


class TestUserService:
    """Tests for UserService."""

    @pytest.fixture
    def user_repository(self) -> Mock:
        return Mock(spec=UserRepository)

    @pytest.fixture
    def email_service(self) -> AsyncMock:
        return AsyncMock(spec=EmailService)

    @pytest.fixture
    def service(
        self,
        user_repository: Mock,
        email_service: AsyncMock,
    ) -> UserService:
        return UserService(user_repository, email_service)

    async def test_create_user_success(
        self,
        service: UserService,
        user_repository: Mock,
        email_service: AsyncMock,
    ) -> None:
        """Should create user and send welcome email."""
        # Arrange
        user_data = UserCreate(
            email="test@example.com",
            name="Test User",
            password="securepassword123",
        )
        expected_user = User(id=1, email=user_data.email, name=user_data.name)
        user_repository.create.return_value = expected_user

        # Act
        result = await service.create_user(user_data)

        # Assert
        assert result == expected_user
        user_repository.create.assert_called_once()
        email_service.send_welcome.assert_awaited_once_with(expected_user)

    async def test_create_user_duplicate_email_raises(
        self,
        service: UserService,
        user_repository: Mock,
    ) -> None:
        """Should raise ConflictError when email already exists."""
        # Arrange
        user_data = UserCreate(
            email="existing@example.com",
            name="Test User",
            password="securepassword123",
        )
        user_repository.find_by_email.return_value = User(id=1, email=user_data.email)

        # Act & Assert
        with pytest.raises(ConflictError) as exc_info:
            await service.create_user(user_data)
        
        assert "email already exists" in str(exc_info.value).lower()


# Parametrized tests for multiple cases
@pytest.mark.parametrize(
    "input_value,expected",
    [
        ("hello", "HELLO"),
        ("World", "WORLD"),
        ("", ""),
        ("123", "123"),
    ],
    ids=["lowercase", "mixed_case", "empty", "numbers"],
)
def test_uppercase_conversion(input_value: str, expected: str) -> None:
    assert input_value.upper() == expected


# Property-based testing with Hypothesis
from hypothesis import given, strategies as st


@given(st.lists(st.integers()))
def test_sort_is_idempotent(xs: list[int]) -> None:
    """Sorting twice should give same result as sorting once."""
    assert sorted(sorted(xs)) == sorted(xs)


@given(st.lists(st.integers()))
def test_sort_preserves_length(xs: list[int]) -> None:
    """Sorting should not change list length."""
    assert len(sorted(xs)) == len(xs)
```

### Fixtures and Factories

```python
# conftest.py
import pytest
from faker import Faker

fake = Faker()


@pytest.fixture
def user_factory() -> Callable[..., User]:
    """Factory for creating test users."""
    def create(
        *,
        id: int | None = None,
        email: str | None = None,
        name: str | None = None,
        is_active: bool = True,
    ) -> User:
        return User(
            id=id or fake.random_int(1, 10000),
            email=email or fake.email(),
            name=name or fake.name(),
            is_active=is_active,
        )
    return create


@pytest.fixture
async def db_session(test_engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    """Provide a transactional database session for tests."""
    async with AsyncSession(test_engine) as session:
        async with session.begin():
            yield session
            await session.rollback()
```

---

## Security Practices

### Input Validation

```python
from pydantic import BaseModel, Field, field_validator, EmailStr
import re


class UserRegistration(BaseModel):
    """Validated user registration input."""
    
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    name: str = Field(min_length=1, max_length=100)

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain digit")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain special character")
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        # Prevent injection attacks
        if re.search(r"[<>&\"']", v):
            raise ValueError("Name contains invalid characters")
        return v.strip()
```

### Secrets Management

```python
import secrets
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Sensitive values from environment
    database_url: str
    secret_key: str
    api_key: str

    # Never log or serialize sensitive fields
    def __repr__(self) -> str:
        return "Settings(***)"


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Generate secure tokens
def generate_token(length: int = 32) -> str:
    """Generate cryptographically secure token."""
    return secrets.token_urlsafe(length)


def generate_otp(length: int = 6) -> str:
    """Generate numeric OTP."""
    return "".join(str(secrets.randbelow(10)) for _ in range(length))
```

### SQL Injection Prevention

```python
from sqlalchemy import select, text
from sqlalchemy.orm import Session


# Always use parameterized queries
# Bad — vulnerable to SQL injection
def find_user_bad(session: Session, email: str) -> User | None:
    query = f"SELECT * FROM users WHERE email = '{email}'"
    return session.execute(text(query)).first()


# Good — parameterized query
def find_user(session: Session, email: str) -> User | None:
    stmt = select(User).where(User.email == email)
    return session.execute(stmt).scalar_one_or_none()


# If raw SQL is necessary, use parameters
def search_users(session: Session, pattern: str) -> list[User]:
    stmt = text("SELECT * FROM users WHERE name ILIKE :pattern")
    result = session.execute(stmt, {"pattern": f"%{pattern}%"})
    return [User.from_row(row) for row in result]
```

### Authentication & Authorization

```python
from datetime import datetime, timedelta
from typing import Annotated

import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta = timedelta(hours=1),
) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm="HS256")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    """Validate token and return current user."""
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = await user_repository.get(user_id)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def require_role(*roles: str) -> Callable:
    """Decorator to require specific roles."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(
            *args,
            current_user: User = Depends(get_current_user),
            **kwargs,
        ):
            if not any(role in current_user.roles for role in roles):
                raise HTTPException(status_code=403, detail="Insufficient permissions")
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator
```

---

## Performance Guidelines

### Memory Efficiency

```python
from collections.abc import Generator, Iterator
from itertools import islice


# Use generators for large datasets
def read_large_file(path: Path) -> Generator[str, None, None]:
    """Read large file line by line without loading into memory."""
    with open(path) as f:
        for line in f:
            yield line.strip()


# Use itertools for efficient iteration
def batch_items(items: Iterator[T], batch_size: int) -> Iterator[list[T]]:
    """Yield items in batches."""
    iterator = iter(items)
    while batch := list(islice(iterator, batch_size)):
        yield batch


# Use __slots__ for memory-critical classes
class Point:
    __slots__ = ("x", "y", "z")
    
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z


# Use array for homogeneous numeric data
from array import array

numbers: array[int] = array("i", range(1000000))  # Much smaller than list
```

### Caching

```python
from functools import cache, lru_cache
from cachetools import TTLCache, cached
from threading import Lock


# Simple memoization
@cache
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


# LRU cache with size limit
@lru_cache(maxsize=1024)
def expensive_computation(x: int, y: int) -> float:
    ...


# TTL cache for external data
_user_cache: TTLCache[int, User] = TTLCache(maxsize=1000, ttl=300)
_cache_lock = Lock()


async def get_user_cached(user_id: int) -> User:
    """Get user with caching."""
    with _cache_lock:
        if user_id in _user_cache:
            return _user_cache[user_id]
    
    user = await fetch_user(user_id)
    
    with _cache_lock:
        _user_cache[user_id] = user
    
    return user


# Async-aware caching
from aiocache import cached as async_cached
from aiocache.serializers import PickleSerializer


@async_cached(ttl=300, serializer=PickleSerializer())
async def fetch_external_data(key: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/{key}")
        return response.json()
```

### Profiling and Optimization

```python
import cProfile
import pstats
from functools import wraps
from time import perf_counter
from typing import Callable, TypeVar

F = TypeVar("F", bound=Callable)


def profile(func: F) -> F:
    """Decorator to profile function execution."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        try:
            return profiler.runcall(func, *args, **kwargs)
        finally:
            stats = pstats.Stats(profiler)
            stats.strip_dirs()
            stats.sort_stats("cumulative")
            stats.print_stats(20)
    return wrapper


def timed(func: F) -> F:
    """Decorator to measure execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed = perf_counter() - start
            print(f"{func.__name__} took {elapsed:.4f}s")
    return wrapper


# Use for optimization hints
if TYPE_CHECKING:
    # Type stubs for Cython-optimized modules
    from _optimized import fast_function
else:
    try:
        from _optimized import fast_function
    except ImportError:
        # Fallback to pure Python
        def fast_function(data: list[int]) -> int:
            return sum(data)
```

---

## Project Structure

### Standard Layout

```
project_name/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── docs/
│   ├── api/
│   ├── guides/
│   └── index.md
├── scripts/
│   ├── setup.sh
│   └── deploy.sh
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── py.typed               # PEP 561 marker
│       ├── core/
│       │   ├── __init__.py
│       │   ├── config.py
│       │   ├── logging.py
│       │   └── exceptions.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── user.py
│       │   └── order.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── user_service.py
│       │   └── order_service.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── deps.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── users.py
│       │   │   └── orders.py
│       │   └── router.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── pyproject.toml
├── README.md
└── uv.lock
```

### pyproject.toml Configuration

```toml
[project]
name = "project-name"
version = "1.0.0"
description = "A professional Python project"
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.11"
authors = [
    { name = "Your Name", email = "you@example.com" }
]
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
    "Typing :: Typed",
]
dependencies = [
    "pydantic>=2.0",
    "httpx>=0.24",
    "sqlalchemy>=2.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "pytest-asyncio>=0.21",
    "pytest-cov>=4.0",
    "mypy>=1.5",
    "ruff>=0.1",
    "pre-commit>=3.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/project_name"]

[tool.ruff]
target-version = "py311"
line-length = 88
src = ["src", "tests"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate
    "PL",     # Pylint
    "RUF",    # Ruff-specific
]
ignore = [
    "PLR0913",  # Too many arguments
    "PLR2004",  # Magic value comparison
]

[tool.ruff.lint.isort]
known-first-party = ["project_name"]

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "-ra",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests requiring external services",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = ["*/tests/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
    "@abstractmethod",
]
fail_under = 80
```

---

## Tooling & Automation

### Pre-commit Configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
      - id: check-merge-conflict

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic
          - types-requests
        args: [--config-file=pyproject.toml]

  - repo: https://github.com/commitizen-tools/commitizen
    rev: v3.12.0
    hooks:
      - id: commitizen
        stages: [commit-msg]
```

### Makefile

```makefile
.PHONY: install dev test lint format type-check clean build

# Development setup
install:
	uv sync

dev:
	uv sync --all-extras

# Testing
test:
	uv run pytest

test-cov:
	uv run pytest --cov --cov-report=html --cov-report=term

test-watch:
	uv run ptw -- --last-failed

# Code quality
lint:
	uv run ruff check src tests

format:
	uv run ruff format src tests
	uv run ruff check --fix src tests

type-check:
	uv run mypy src

check: lint type-check test

# Cleaning
clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Building
build:
	uv build

# Documentation
docs:
	uv run mkdocs serve

docs-build:
	uv run mkdocs build
```

### GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
        
      - name: Set up Python
        run: uv python install 3.12
        
      - name: Install dependencies
        run: uv sync --all-extras
        
      - name: Run linting
        run: uv run ruff check src tests
        
      - name: Run formatting check
        run: uv run ruff format --check src tests
        
      - name: Run type checking
        run: uv run mypy src

  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Install uv
        uses: astral-sh/setup-uv@v1
        
      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}
        
      - name: Install dependencies
        run: uv sync --all-extras
        
      - name: Run tests
        run: uv run pytest --cov --cov-report=xml
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

---

## Quick Reference Card

### Do's ✓

- Use type hints everywhere
- Write docstrings for public APIs
- Use `dataclass` or `attrs` for data containers
- Prefer composition over inheritance
- Use `async/await` for I/O operations
- Write tests for all business logic
- Use `pathlib.Path` instead of string paths
- Use `logging` instead of `print`
- Use context managers for resource cleanup
- Follow semantic versioning

### Don'ts ✗

- No wildcard imports (`from x import *`)
- No mutable default arguments
- No bare `except:` clauses
- No single-letter variable names (except in comprehensions)
- No `type: ignore` without explanation
- No blocking calls in async code
- No secrets in code or version control
- No raw SQL without parameterization
- No deeply nested code (max 3-4 levels)
- No functions longer than 50 lines

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Dec 2025 | Initial release |

---

**Document maintained by:** Engineering Team  
**Review cycle:** Quarterly  
**Last review:** December 2025

---

*"Programs must be written for people to read, and only incidentally for machines to execute."*  
— Harold Abelson