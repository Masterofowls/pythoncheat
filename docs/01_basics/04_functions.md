# Python Functions

## Basic Function Definition

```python
def greet(name):
    """Simple function that returns a greeting"""
    return f"Hello, {name}!"

# Calling the function
message = greet("Alice")  # "Hello, Alice!"
```

## Parameters and Arguments

### Default Parameters
```python
def power(base, exponent=2):
    return base ** exponent

square = power(4)      # 16 (exponent defaults to 2)
cube = power(4, 3)     # 64 (exponent specified as 3)
```

### Keyword Arguments
```python
def create_user(name, age, city="Unknown"):
    return {"name": name, "age": age, "city": city}

# Different ways to call
user1 = create_user("John", 25, "New York")
user2 = create_user(age=30, name="Alice")  # Order doesn't matter with keyword args
user3 = create_user("Bob", age=35)         # Mix positional and keyword args
```

### Variable Number of Arguments
```python
# *args for variable positional arguments
def sum_all(*numbers):
    return sum(numbers)

result = sum_all(1, 2, 3, 4)  # 10

# **kwargs for variable keyword arguments
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="John", age=30, city="New York")
```

## Return Values

```python
# Multiple return values
def get_coordinates():
    return 5, 10  # Returns a tuple

x, y = get_coordinates()  # Tuple unpacking

# Return different types
def process_number(num):
    if num < 0:
        return None
    elif num == 0:
        return False
    else:
        return num * 2
```

## Function Annotations (Type Hints)

```python
from typing import List, Optional, Dict, Any

def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """Calculate basic statistics from a list of numbers."""
    return {
        "mean": sum(numbers) / len(numbers),
        "max": max(numbers),
        "min": min(numbers)
    }

def greet_user(name: str, age: Optional[int] = None) -> str:
    if age is None:
        return f"Hello {name}!"
    return f"Hello {name}, you are {age} years old!"
```

## Lambda Functions

```python
# Simple lambda function
square = lambda x: x ** 2

# Lambda with multiple parameters
multiply = lambda x, y: x * y

# Lambda in sorting
pairs = [(1, 'one'), (2, 'two'), (3, 'three')]
sorted_pairs = sorted(pairs, key=lambda pair: pair[1])  # Sort by string
```

## Decorators

```python
from functools import wraps
import time

# Simple timing decorator
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)
    return "Done!"
```

## Generators

```python
def fibonacci(n):
    """Generate first n Fibonacci numbers"""
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

# Using the generator
for num in fibonacci(10):
    print(num)
```

## Function Scope and Closure

```python
def outer_function(x):
    def inner_function(y):
        return x + y  # x is from the enclosing scope
    return inner_function

add_five = outer_function(5)
result = add_five(3)  # 8
```

## Best Practices

1. Function Naming
   - Use lowercase with underscores (snake_case)
   - Be descriptive but concise
   - Use verbs for functions that perform actions

```python
# Good
def calculate_total_price(items):
    pass

# Avoid
def TCP(i):  # Too short and unclear
    pass
```

2. Documentation
   - Use docstrings for function documentation
   - Include parameter types, return types, and examples

```python
def divide(a: float, b: float) -> float:
    """
    Divide two numbers.

    Args:
        a (float): The dividend
        b (float): The divisor

    Returns:
        float: The result of a/b

    Raises:
        ZeroDivisionError: If b is zero
    """
    return a / b
```

3. Single Responsibility
   - Each function should do one thing well
   - Keep functions short and focused

4. Parameter Rules
   - Limit the number of parameters (≤ 4 is ideal)
   - Use default values appropriately
   - Consider using data classes for many parameters

## Common Pitfalls

### Mutable Default Arguments
```python
# Bad
def add_item(item, items=[]):  # List created once at definition
    items.append(item)
    return items

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Late Binding Closures
```python
# Bad
def create_multipliers():
    return [lambda x: i * x for i in range(4)]

# Good
def create_multipliers():
    return [lambda x, i=i: i * x for i in range(4)]
```

## Practice Examples

```python
# 1. Function with validation
def divide_safe(a: float, b: float) -> Optional[float]:
    try:
        return a / b
    except ZeroDivisionError:
        return None

# 2. Decorator with parameters
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    print(f"Hello {name}")

# 3. Context manager as generator
from contextlib import contextmanager

@contextmanager
def timer():
    start = time.time()
    yield
    end = time.time()
    print(f"Elapsed time: {end - start:.2f} seconds")
```

## Exercises

1. Create a decorator that caches function results
2. Write a generator that yields prime numbers
3. Implement a function that accepts both positional and keyword arguments
4. Create a closure that maintains a running average
5. Write a function using type hints and document it properly