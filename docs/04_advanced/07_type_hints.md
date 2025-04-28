# Python Type Hints

## Basic Types

### Built-in Types
```python
def greet(name: str) -> str:
    return f"Hello, {name}"

def calculate_age(birth_year: int) -> int:
    return 2025 - birth_year

def is_adult(age: int) -> bool:
    return age >= 18

def get_price(amount: float) -> str:
    return f"${amount:.2f}"
```

### Collections
```python
from typing import List, Dict, Set, Tuple

def process_numbers(numbers: List[int]) -> int:
    return sum(numbers)

def get_user_data() -> Dict[str, str]:
    return {"name": "John", "email": "john@example.com"}

def unique_tags(tags: Set[str]) -> int:
    return len(tags)

def get_coordinates() -> Tuple[float, float]:
    return (40.7128, -74.0060)
```

## Optional and Union Types

### Optional Values
```python
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    users = {1: "John", 2: "Jane"}
    return users.get(user_id)

def greet_user(name: Optional[str] = None) -> str:
    if name is None:
        return "Hello, Guest"
    return f"Hello, {name}"
```

### Union Types
```python
from typing import Union

def process_data(data: Union[str, bytes]) -> str:
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data

def format_number(num: Union[int, float]) -> str:
    return f"{num:.2f}"
```

## Generic Types

### Type Variables
```python
from typing import TypeVar, List

T = TypeVar('T')

def first_element(lst: List[T]) -> Optional[T]:
    return lst[0] if lst else None

def swap_elements(a: T, b: T) -> Tuple[T, T]:
    return b, a
```

### Generic Classes
```python
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.items: List[T] = []
    
    def push(self, item: T) -> None:
        self.items.append(item)
    
    def pop(self) -> Optional[T]:
        return self.items.pop() if self.items else None
    
    def peek(self) -> Optional[T]:
        return self.items[-1] if self.items else None
```

## Protocol Types

### Basic Protocol
```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None:
        ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    def draw(self) -> None:
        print("Drawing square")

def render(shape: Drawable) -> None:
    shape.draw()
```

### Complex Protocol
```python
from typing import Protocol, Iterator

class Openable(Protocol):
    def open(self) -> None:
        ...
    def close(self) -> None:
        ...
    def read(self) -> str:
        ...

class File:
    def open(self) -> None:
        pass
    def close(self) -> None:
        pass
    def read(self) -> str:
        return "file contents"

def process_file(file: Openable) -> str:
    file.open()
    try:
        return file.read()
    finally:
        file.close()
```

## Type Aliases

### Simple Aliases
```python
from typing import Dict, List, Union

JSON = Dict[str, Union[str, int, float, bool, None]]
Vector = List[float]
Matrix = List[Vector]

def process_json(data: JSON) -> None:
    pass

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    pass
```

### Complex Aliases
```python
from typing import Callable, TypeVar

T = TypeVar('T')
Predicate = Callable[[T], bool]
Transformer = Callable[[T], T]

def filter_list(lst: List[T], pred: Predicate[T]) -> List[T]:
    return [x for x in lst if pred(x)]

def transform_list(lst: List[T], func: Transformer[T]) -> List[T]:
    return [func(x) for x in lst]
```

## Type Checking

### Runtime Checks
```python
from typing import cast, Any

def process_string(s: Any) -> str:
    # Runtime type check
    if not isinstance(s, str):
        raise TypeError("Expected str")
    return s.upper()

def safe_divide(a: Any, b: Any) -> float:
    # Type casting
    x = cast(float, a)
    y = cast(float, b)
    return x / y
```

### Static Type Checking
```python
# mypy configuration
"""
[mypy]
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
disallow_untyped_decorators = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
warn_return_any = True
warn_unreachable = True
strict_optional = True
"""

# Type-checked function
def calculate_average(numbers: List[float]) -> float:
    if not numbers:
        raise ValueError("Empty list")
    return sum(numbers) / len(numbers)
```

## Best Practices

### Type Documentation
```python
from typing import Dict, List, Optional

class User:
    """
    Represents a user in the system.
    
    Attributes:
        name (str): The user's full name
        email (str): The user's email address
        age (Optional[int]): The user's age, if known
    """
    def __init__(
        self,
        name: str,
        email: str,
        age: Optional[int] = None
    ) -> None:
        self.name = name
        self.email = email
        self.age = age

    def to_dict(self) -> Dict[str, Union[str, Optional[int]]]:
        """
        Convert user to dictionary representation.
        
        Returns:
            Dict containing user data with typed keys and values.
        """
        return {
            "name": self.name,
            "email": self.email,
            "age": self.age
        }
```

### Type Safety
```python
from typing import overload, Union

class SafeList:
    """A type-safe list implementation."""
    
    @overload
    def __getitem__(self, index: int) -> T: ...
    
    @overload
    def __getitem__(self, index: slice) -> List[T]: ...
    
    def __getitem__(
        self,
        index: Union[int, slice]
    ) -> Union[T, List[T]]:
        if isinstance(index, slice):
            return self.items[index]
        return self.items[index]
```

## Exercises

1. Create a generic cache implementation with type hints
2. Implement a type-safe event system using Protocols
3. Build a data validation system using type hints
4. Create a type-safe API client with proper error handling
5. Implement a generic tree structure with type hints