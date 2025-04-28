# Python Type Hints

## Basic Type Hints

### Variable Annotations
```python
from typing import List, Dict, Set, Tuple

# Basic type hints
name: str = "John"
age: int = 30
height: float = 1.75
is_active: bool = True

# Container types
numbers: List[int] = [1, 2, 3]
pairs: Dict[str, int] = {"one": 1, "two": 2}
unique_items: Set[str] = {"apple", "banana"}
coordinates: Tuple[float, float] = (1.0, 2.0)
```

### Function Annotations
```python
from typing import Optional, Union

def greet(name: str) -> str:
    """Basic function with type hints"""
    return f"Hello, {name}"

def process_data(data: Optional[str] = None) -> Union[str, None]:
    """Function with optional parameter"""
    if data is None:
        return None
    return data.upper()

def calculate_total(items: List[float], tax_rate: float = 0.1) -> float:
    """Function with container type hint"""
    subtotal = sum(items)
    return subtotal * (1 + tax_rate)
```

## Advanced Type Hints

### Custom Types
```python
from typing import TypeVar, Generic, NewType

# Type variables
T = TypeVar('T')
Number = TypeVar('Number', int, float)

# Custom types
UserId = NewType('UserId', int)
Email = NewType('Email', str)

class Box(Generic[T]):
    """Generic container class"""
    def __init__(self, item: T) -> None:
        self.item = item
    
    def get(self) -> T:
        return self.item

# Using custom types
user_id: UserId = UserId(123)
email: Email = Email("user@example.com")
int_box: Box[int] = Box(42)
str_box: Box[str] = Box("Hello")
```

### Complex Types
```python
from typing import Callable, Iterator, Generator, Any

# Function types
Handler = Callable[[str, int], bool]

def process_with_handler(data: str, handler: Handler) -> bool:
    """Function using callable type"""
    return handler(data, len(data))

# Iterator types
def count_up(limit: int) -> Iterator[int]:
    """Function returning iterator"""
    counter = 0
    while counter < limit:
        yield counter
        counter += 1

# Generator types
def number_generator() -> Generator[int, None, None]:
    """Generator function with type hints"""
    yield from range(10)

# Any type
def process_any(data: Any) -> Any:
    """Function accepting any type"""
    return data
```

### Type Aliases
```python
from typing import Union, Dict, List

# Complex type aliases
JsonDict = Dict[str, Union[str, int, float, bool, None]]
Matrix = List[List[float]]
NestedDict = Dict[str, Union[str, 'NestedDict']]

def process_json(data: JsonDict) -> str:
    """Process JSON-like dictionary"""
    return str(data)

def matrix_multiply(a: Matrix, b: Matrix) -> Matrix:
    """Matrix multiplication with type hints"""
    # Implementation omitted
    return [[0.0]]

def process_nested(data: NestedDict) -> None:
    """Process nested dictionary structure"""
    pass
```

## Practical Applications

### Class Typing
```python
from typing import ClassVar, Final
from dataclasses import dataclass

class Configuration:
    """Class with type hints"""
    DEBUG: ClassVar[bool] = False  # Class variable
    API_KEY: Final[str] = "secret"  # Constant
    
    def __init__(self, host: str, port: int) -> None:
        self.host: str = host
        self.port: int = port
    
    @classmethod
    def create_default(cls) -> 'Configuration':
        return cls("localhost", 8080)

@dataclass
class User:
    """Dataclass with type hints"""
    name: str
    age: int
    email: Optional[str] = None
```

### Protocol Types
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    """Protocol defining drawable interface"""
    def draw(self) -> None:
        """Draw the object"""
        ...

class Circle:
    """Class implementing Drawable protocol"""
    def draw(self) -> None:
        print("Drawing circle")

class Square:
    """Another class implementing Drawable protocol"""
    def draw(self) -> None:
        print("Drawing square")

def draw_shape(shape: Drawable) -> None:
    """Function accepting any Drawable object"""
    shape.draw()
```

### Type Guards
```python
from typing import TypeGuard, Union, overload

def is_string_list(value: List[Any]) -> TypeGuard[List[str]]:
    """Type guard for list of strings"""
    return all(isinstance(x, str) for x in value)

def process_strings(items: List[Any]) -> None:
    """Function using type guard"""
    if is_string_list(items):
        # Type checker knows items is List[str]
        for item in items:
            print(item.upper())

@overload
def get_value(key: str) -> str: ...
@overload
def get_value(key: int) -> int: ...

def get_value(key: Union[str, int]) -> Union[str, int]:
    """Function with multiple signatures"""
    return str(key) if isinstance(key, str) else key
```

## Best Practices

### Type Comments
```python
# Python 2 compatibility
def legacy_function(name, age):
    # type: (str, int) -> str
    return f"{name} is {age} years old"

# Variable type comments
x = []  # type: List[int]
```

### Optional and Union
```python
from typing import Optional, Union

def process_input(data: Optional[str]) -> Union[str, int]:
    """Function with optional input and union return"""
    if data is None:
        return 0
    return data.upper()

def update_record(
    name: str,
    age: Optional[int] = None,
    email: Union[str, None] = None
) -> None:
    """Function with multiple optional parameters"""
    pass
```

### Type Ignore Comments
```python
# Ignore all errors in file
# type: ignore

# Ignore specific error
x = "hello"  # type: ignore[assignment]

# Ignore import error
from module import missing  # type: ignore[import]
```

## Common Patterns

### Factory Functions
```python
from typing import TypeVar, Type

T = TypeVar('T')

class Animal:
    def speak(self) -> str:
        return "Generic animal sound"

class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"

def create_animal(animal_type: Type[T]) -> T:
    """Factory function with generic type"""
    return animal_type()

# Using factory function
dog: Dog = create_animal(Dog)
```

### Container Types
```python
from typing import Sequence, Mapping, MutableMapping

def process_sequence(seq: Sequence[int]) -> List[int]:
    """Function accepting any sequence type"""
    return list(reversed(seq))

def update_mapping(
    data: MutableMapping[str, int],
    updates: Mapping[str, int]
) -> None:
    """Function working with mapping types"""
    for key, value in updates.items():
        data[key] = value
```

## Exercises

1. Implement a generic cache decorator with type hints
2. Create a type-safe event system using Protocol
3. Design a configuration system with typed settings
4. Implement a generic repository pattern with type hints
5. Create a type-safe builder pattern implementation