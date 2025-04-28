# Functional Programming in Python

## Core Concepts

### Pure Functions
```python
# Pure function - same input always produces same output
def multiply(x: int, y: int) -> int:
    return x * y

# Impure function - result depends on external state
counter = 0
def increment() -> int:
    global counter
    counter += 1
    return counter
```

### Immutability
```python
from typing import Tuple, List, Dict
from dataclasses import dataclass
from collections.abc import Sequence

# Immutable data structures
@dataclass(frozen=True)
class Point:
    x: float
    y: float
    
    def move(self, dx: float, dy: float) -> 'Point':
        """Returns new instance instead of modifying"""
        return Point(self.x + dx, self.y + dy)

# Immutable sequences
def process_data(data: Tuple[int, ...]) -> Tuple[int, ...]:
    return tuple(x * 2 for x in data)
```

### Higher-Order Functions
```python
from typing import Callable, TypeVar, List, Any
from functools import partial, reduce

T = TypeVar('T')
U = TypeVar('U')

def compose(f: Callable[[U], T], g: Callable[[Any], U]) -> Callable[[Any], T]:
    """Function composition"""
    return lambda x: f(g(x))

def pipe(value: T, *functions: Callable) -> Any:
    """Function pipeline"""
    return reduce(lambda v, f: f(v), functions, value)

# Example usage
def double(x: int) -> int:
    return x * 2

def increment(x: int) -> int:
    return x + 1

# Compose functions
double_then_increment = compose(increment, double)
increment_then_double = compose(double, increment)

print(double_then_increment(5))      # 11
print(increment_then_double(5))      # 12
```

## Functional Tools

### Map, Filter, Reduce
```python
from typing import TypeVar, List, Callable
from functools import reduce
from operator import add

T = TypeVar('T')
U = TypeVar('U')

# Map example
numbers: List[int] = [1, 2, 3, 4, 5]
squared = list(map(lambda x: x * x, numbers))

# Filter example
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))

# Reduce example
sum_numbers = reduce(add, numbers)

# Combining operations
result = reduce(
    add,
    filter(lambda x: x % 2 == 0, 
           map(lambda x: x * x, numbers))
)
```

### Partial Application
```python
from typing import Callable
from functools import partial

def greet(prefix: str, name: str) -> str:
    return f"{prefix} {name}!"

# Create specialized functions
greet_mr = partial(greet, "Mr.")
greet_ms = partial(greet, "Ms.")

print(greet_mr("Smith"))    # Mr. Smith!
print(greet_ms("Johnson"))  # Ms. Johnson!
```

### Decorators as Higher-Order Functions
```python
from typing import Callable, TypeVar, Any
from functools import wraps
import time

T = TypeVar('T')

def memoize(func: Callable[..., T]) -> Callable[..., T]:
    """Memoization decorator"""
    cache = {}
    
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    return wrapper

@memoize
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

## Advanced Functional Patterns

### Monads
```python
from typing import TypeVar, Generic, Callable, Optional
from dataclasses import dataclass

T = TypeVar('T')
U = TypeVar('U')

@dataclass
class Maybe(Generic[T]):
    """Maybe monad implementation"""
    value: Optional[T]
    
    @staticmethod
    def just(value: T) -> 'Maybe[T]':
        return Maybe(value)
    
    @staticmethod
    def nothing() -> 'Maybe[T]':
        return Maybe(None)
    
    def bind(self, f: Callable[[T], 'Maybe[U]']) -> 'Maybe[U]':
        if self.value is None:
            return Maybe.nothing()
        return f(self.value)
    
    def map(self, f: Callable[[T], U]) -> 'Maybe[U]':
        if self.value is None:
            return Maybe.nothing()
        return Maybe.just(f(self.value))

# Example usage
def safe_divide(x: float, y: float) -> Maybe[float]:
    if y == 0:
        return Maybe.nothing()
    return Maybe.just(x / y)

def safe_sqrt(x: float) -> Maybe[float]:
    if x < 0:
        return Maybe.nothing()
    return Maybe.just(x ** 0.5)

# Chain operations safely
result = (Maybe.just(16.0)
         .bind(lambda x: safe_divide(x, 4))
         .bind(safe_sqrt))
```

### Function Composition with Generators
```python
from typing import Iterator, TypeVar, Callable, Iterable

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

def compose_gen(f: Callable[[T], U], 
                g: Callable[[U], V]) -> Callable[[Iterator[T]], Iterator[V]]:
    """Compose functions that work with iterators"""
    def composed(it: Iterator[T]) -> Iterator[V]:
        return (f(x) for x in map(g, it))
    return composed

def chunk(size: int) -> Callable[[Iterator[T]], Iterator[List[T]]]:
    """Create chunks of size n"""
    def chunker(it: Iterator[T]) -> Iterator[List[T]]:
        chunk = []
        for item in it:
            chunk.append(item)
            if len(chunk) == size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk
    return chunker

# Example usage
numbers = range(10)
process = compose_gen(
    lambda x: x * 2,
    lambda x: x + 1
)
chunked = chunk(3)(process(numbers))
```

## Best Practices

1. Prefer Pure Functions
   - Avoid side effects
   - Make dependencies explicit
   - Return new objects instead of modifying

2. Use Type Hints
   - Make function signatures clear
   - Enable better tooling support
   - Document expected types

3. Leverage Standard Library
   - Use functools module
   - Utilize itertools for iteration
   - Apply operator module functions

4. Performance Considerations
   - Use generators for large datasets
   - Consider memoization for expensive operations
   - Profile recursive functions

## Common Patterns

### Function Composition
```python
from typing import Callable, TypeVar
from functools import reduce

T = TypeVar('T')

def compose(*functions: Callable) -> Callable:
    """Compose multiple functions"""
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

# Usage
processed = compose(str.strip, str.lower, str.capitalize)
result = processed("  HELLO WORLD  ")  # "Hello world"
```

### Pipeline Pattern
```python
from typing import Any, Callable
from dataclasses import dataclass
from functools import reduce

@dataclass
class Pipeline:
    """Data processing pipeline"""
    functions: List[Callable]
    
    def __call__(self, value: Any) -> Any:
        return reduce(lambda v, f: f(v), 
                     self.functions, 
                     value)
    
    def add_step(self, func: Callable) -> 'Pipeline':
        return Pipeline(self.functions + [func])

# Usage
pipeline = Pipeline([
    lambda x: x * 2,
    lambda x: x + 1,
    lambda x: f"Result: {x}"
])
result = pipeline(5)  # "Result: 11"
```

## Exercises

1. Implement a lazy evaluation decorator
2. Create a function composition utility
3. Build a Maybe monad for error handling
4. Design a data processing pipeline
5. Practice with higher-order functions