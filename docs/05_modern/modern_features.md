# Modern Python Features

## Type Hints and Static Typing

### Basic Type Annotations
```python
from typing import List, Dict, Optional, Union, Any

def process_data(items: List[int], config: Dict[str, Any]) -> Optional[str]:
    """Function with type hints"""
    if not items:
        return None
    return str(sum(items))

# Variable annotations
name: str = "Python"
age: int = 30
data: List[Dict[str, Any]] = []
```

### Generic Types
```python
from typing import TypeVar, Generic, Sequence

T = TypeVar('T')
U = TypeVar('U')

class DataContainer(Generic[T]):
    def __init__(self, data: T):
        self.data = data
    
    def get_data(self) -> T:
        return self.data
    
    def map(self, func: Callable[[T], U]) -> 'DataContainer[U]':
        return DataContainer(func(self.data))

# Using generics
numbers = DataContainer[int](42)
text = numbers.map(str)  # DataContainer[str]
```

## Pattern Matching (Python 3.10+)

### Basic Pattern Matching
```python
def process_command(command: str) -> str:
    match command.split():
        case ["quit"]:
            return "Exiting..."
        case ["help"]:
            return "Available commands: quit, help"
        case ["add", *numbers]:
            return str(sum(map(int, numbers)))
        case _:
            return "Unknown command"
```

### Structural Pattern Matching
```python
from dataclasses import dataclass
from typing import List

@dataclass
class Point:
    x: float
    y: float

def process_shape(shape: dict) -> str:
    match shape:
        case {"type": "circle", "radius": radius}:
            return f"Circle with radius {radius}"
        case {"type": "rectangle", "width": w, "height": h}:
            return f"Rectangle {w}x{h}"
        case {"type": "polygon", "points": points}:
            return f"Polygon with {len(points)} points"
        case _:
            return "Unknown shape"
```

## Asynchronous Features

### Basic Async/Await
```python
import asyncio
from typing import List

async def fetch_data(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def process_urls(urls: List[str]) -> List[str]:
    tasks = [fetch_data(url) for url in urls]
    return await asyncio.gather(*tasks)
```

### Async Context Managers
```python
from contextlib import asynccontextmanager
from typing import AsyncIterator

@asynccontextmanager
async def managed_resource() -> AsyncIterator[str]:
    print("Acquiring resource")
    try:
        yield "resource"
    finally:
        print("Releasing resource")

async def use_resource() -> None:
    async with managed_resource() as resource:
        print(f"Using {resource}")
```

## Advanced Function Features

### Positional-Only and Keyword-Only Arguments
```python
def calculate(x: float, y: float, /, *, operation: str = "add") -> float:
    """
    x and y are positional-only (before /)
    operation is keyword-only (after *)
    """
    match operation:
        case "add":
            return x + y
        case "multiply":
            return x * y
        case _:
            raise ValueError(f"Unknown operation: {operation}")
```

### Function Type Hints with Protocols
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...

def render(item: Drawable) -> None:
    item.draw()

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

# Circle implements Drawable protocol
circle = Circle()
render(circle)  # Type checks pass
```

## Advanced Data Classes

### Extended Dataclass Features
```python
from dataclasses import dataclass, field
from typing import List, ClassVar

@dataclass(frozen=True, order=True)
class Product:
    name: str
    price: float
    tags: List[str] = field(default_factory=list)
    inventory: int = field(init=False, default=0)
    tax_rate: ClassVar[float] = 0.1
    
    def __post_init__(self) -> None:
        # Can modify even frozen dataclass during initialization
        object.__setattr__(self, 'inventory', 10)
    
    @property
    def total_price(self) -> float:
        return self.price * (1 + self.tax_rate)
```

## Modern String Features

### F-strings with Debugging
```python
name = "Python"
version = 3.10
print(f"{name=}, {version=}")  # name='Python', version=3.10

# Format specifiers in f-strings
number = 123.456
print(f"{number:.2f}")  # 123.46
print(f"{number=:.2f}")  # number=123.46
```

### Advanced String Operations
```python
# Improved string handling
text = """
    Multiline
    string with
    whitespace
"""
cleaned = text.strip()  # Remove leading/trailing whitespace
lines = cleaned.splitlines()  # Split into lines

# String methods
print("Hello".center(20, '-'))  # -----Hello-----
print("Hello".ljust(10, '*'))   # Hello*****
print("123".zfill(5))          # 00123
```

## Best Practices

1. Type Hints Usage
   - Use type hints for better code documentation
   - Enable static type checking with mypy
   - Consider runtime type checking when needed

2. Modern Syntax Features
   - Use pattern matching for complex conditionals
   - Leverage f-strings for string formatting
   - Use walrus operator (:=) for assignment expressions

3. Async Programming
   - Use async/await for IO-bound operations
   - Consider asyncio for concurrent operations
   - Use aiohttp for async HTTP requests

4. Performance Optimization
   - Use profile-guided optimization
   - Leverage modern garbage collection features
   - Use memory views for efficient array operations

## Common Patterns

### Context Manager Pattern
```python
from typing import Iterator, Any

class ManagedResource:
    def __init__(self, name: str):
        self.name = name
    
    def __enter__(self) -> 'ManagedResource':
        print(f"Acquiring {self.name}")
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        print(f"Releasing {self.name}")

# Using the context manager
with ManagedResource("database") as resource:
    print("Using resource")
```

### Singleton Pattern with Type Hints
```python
from typing import Optional

class Singleton:
    _instance: Optional['Singleton'] = None
    
    def __new__(cls) -> 'Singleton':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def get_instance(cls) -> 'Singleton':
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
```

## Exercises

1. Implement a generic cache decorator with type hints
2. Create a pattern-matching based command parser
3. Build an async context manager for resource management
4. Design a type-safe event system using protocols
5. Implement a data container with generic types