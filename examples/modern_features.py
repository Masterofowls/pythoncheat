"""
Modern Python features demonstrated with practical examples.
Shows real-world usage of type hints, pattern matching, async features, and more.
"""
from __future__ import annotations
from typing import (
    TypeVar, Generic, Protocol, runtime_checkable,
    Dict, List, Optional, AsyncIterator, Any
)
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import aiohttp
import json
from decimal import Decimal
from functools import cached_property
from collections.abc import Iterator

T = TypeVar('T')
U = TypeVar('U')

# Modern Type Hints with Generics
class Cache(Generic[T]):
    """Generic cache implementation with type safety"""
    
    def __init__(self, timeout: int = 3600):
        self._data: Dict[str, tuple[T, float]] = {}
        self.timeout = timeout
    
    def get(self, key: str) -> Optional[T]:
        """Get value with type safety"""
        if key in self._data:
            value, timestamp = self._data[key]
            if datetime.now().timestamp() - timestamp < self.timeout:
                return value
            del self._data[key]
        return None
    
    def set(self, key: str, value: T) -> None:
        """Set value with type safety"""
        self._data[key] = (value, datetime.now().timestamp())

# Protocol for Type-Safe Duck Typing
@runtime_checkable
class Serializable(Protocol):
    """Protocol for objects that can be serialized to JSON"""
    def to_json(self) -> str: ...
    def from_json(self, data: str) -> None: ...

@dataclass
class User(Serializable):
    """User class implementing Serializable protocol"""
    name: str
    email: str
    age: int
    tags: List[str] = field(default_factory=list)
    
    def to_json(self) -> str:
        return json.dumps({
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'tags': self.tags
        })
    
    def from_json(self, data: str) -> None:
        user_dict = json.loads(data)
        self.name = user_dict['name']
        self.email = user_dict['email']
        self.age = user_dict['age']
        self.tags = user_dict['tags']

# Pattern Matching for Command Processing
def process_command(command: str) -> str:
    """Process commands using pattern matching"""
    match command.split():
        case ['user', 'create', name, email, age]:
            return f"Creating user: {name}, {email}, {age}"
        case ['user', 'delete', user_id]:
            return f"Deleting user: {user_id}"
        case ['user', 'list']:
            return "Listing all users"
        case ['help', *topics] if topics:
            return f"Help for topics: {', '.join(topics)}"
        case ['help']:
            return "General help"
        case _:
            return "Unknown command"

# Async Features with Context Management
class AsyncResourceManager:
    """Demonstrates async context management"""
    
    def __init__(self, url: str):
        self.url = url
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self) -> AsyncResourceManager:
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        if self.session:
            await self.session.close()
    
    async def fetch_data(self) -> dict:
        """Fetch data using async HTTP"""
        if not self.session:
            raise RuntimeError("Session not initialized")
        
        async with self.session.get(self.url) as response:
            return await response.json()

# Advanced Data Classes with Validation
@dataclass
class Product:
    """Product with price validation and calculations"""
    name: str
    price: Decimal
    quantity: int = 0
    discount: Optional[Decimal] = None
    
    def __post_init__(self) -> None:
        """Validate data after initialization"""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if self.quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if self.discount and (self.discount < 0 or self.discount > 100):
            raise ValueError("Discount must be between 0 and 100")
    
    @cached_property
    def total_price(self) -> Decimal:
        """Calculate total price with caching"""
        if not self.discount:
            return self.price * self.quantity
        discount_multiplier = (100 - self.discount) / 100
        return self.price * self.quantity * discount_multiplier

# Iterator with Type Hints
class PageIterator(Iterator[List[T]]):
    """Type-safe pagination iterator"""
    
    def __init__(self, items: List[T], page_size: int):
        self.items = items
        self.page_size = page_size
        self.current_page = 0
    
    def __next__(self) -> List[T]:
        start = self.current_page * self.page_size
        if start >= len(self.items):
            raise StopIteration
        
        self.current_page += 1
        return self.items[start:start + self.page_size]

async def demonstrate_features() -> None:
    """Demonstrate usage of modern Python features"""
    # Generic cache usage
    cache: Cache[User] = Cache[User](timeout=60)
    user = User("John", "john@example.com", 30)
    cache.set("user1", user)
    cached_user = cache.get("user1")
    
    # Pattern matching
    commands = [
        "user create john john@example.com 30",
        "user list",
        "help user profile",
        "unknown command"
    ]
    for cmd in commands:
        print(f"Command '{cmd}': {process_command(cmd)}")
    
    # Async resource management
    async with AsyncResourceManager("https://api.github.com") as manager:
        try:
            data = await manager.fetch_data()
            print("Fetched data successfully")
        except Exception as e:
            print(f"Error fetching data: {e}")
    
    # Product with validation
    try:
        product = Product("Laptop", Decimal("999.99"), 5, Decimal("10"))
        print(f"Total price: ${product.total_price}")
    except ValueError as e:
        print(f"Validation error: {e}")
    
    # Pagination
    items = list(range(100))
    paginator = PageIterator(items, page_size=10)
    for page in paginator:
        print(f"Page size: {len(page)}")

if __name__ == '__main__':
    asyncio.run(demonstrate_features())