# Python Decorators

## Basic Decorators

### Function Decorators
```python
def timer(func):
    """Decorator that prints the execution time of a function"""
    from time import time
    from functools import wraps
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        end_time = time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds")
        return result
    
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(1)
    return "Done!"

# Using the decorator
result = slow_function()  # prints execution time
```

### Multiple Decorators
```python
def bold(func):
    @wraps(func)
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

@bold
@italic
def greet():
    return "Hello, World!"

print(greet())  # <b><i>Hello, World!</i></b>
```

## Decorator Arguments

### Decorators with Parameters
```python
def repeat(times):
    """Decorator that repeats a function call n times"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(3)
def greet(name):
    return f"Hello {name}"

print(greet("Alice"))  # ['Hello Alice', 'Hello Alice', 'Hello Alice']
```

### Parameterized Decorator Pattern
```python
def validate_types(**type_args):
    """Decorator that validates function argument types"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check positional arguments
            for arg, expected_type in zip(args, type_args.values()):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Expected {expected_type}, got {type(arg)}")
            
            # Check keyword arguments
            for arg_name, arg_value in kwargs.items():
                if arg_name in type_args:
                    expected_type = type_args[arg_name]
                    if not isinstance(arg_value, expected_type):
                        raise TypeError(f"Expected {expected_type}, got {type(arg_value)}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def create_user(name, age):
    return {"name": name, "age": age}

# Valid call
user = create_user("Alice", 30)

# TypeError: Expected <class 'int'>, got <class 'str'>
# user = create_user("Alice", "30")
```

## Class Decorators

### Basic Class Decorator
```python
def singleton(cls):
    """Decorator that ensures a class has only one instance"""
    instances = {}
    
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("Initializing database connection")
    
    def query(self, sql):
        print(f"Executing: {sql}")

# Only creates one instance
db1 = Database()
db2 = Database()  # Returns the same instance
print(db1 is db2)  # True
```

### Class Decorator with Arguments
```python
def dataclass_with_defaults(**default_values):
    """Decorator that adds default values to class attributes"""
    def decorator(cls):
        for name, value in default_values.items():
            setattr(cls, name, value)
        return cls
    return decorator

@dataclass_with_defaults(database="sqlite", port=5432)
class Config:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

config = Config(database="mysql")
print(config.database)  # "mysql"
print(config.port)     # 5432
```

## Method Decorators

### Property Decorator
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get the circle's radius"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set the circle's radius"""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
    
    @property
    def area(self):
        """Calculate the circle's area"""
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.area)  # Access as property
circle.radius = 10  # Use setter
```

### Class Method Decorator
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_str):
        """Create Date from string YYYY-MM-DD"""
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Create Date with today's date"""
        import datetime
        today = datetime.date.today()
        return cls(today.year, today.month, today.day)

date = Date.from_string('2025-04-28')
today = Date.today()
```

## Advanced Patterns

### Decorator Chaining
```python
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

def validate_positive(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if any(arg <= 0 for arg in args if isinstance(arg, (int, float))):
            raise ValueError("Arguments must be positive")
        return func(*args, **kwargs)
    return wrapper

@log_calls
@validate_positive
def calculate_area(width, height):
    return width * height

result = calculate_area(5, 3)  # Logs call and validates arguments
```

### Decorator Classes
```python
class Memoize:
    """Class-based decorator for memoization"""
    def __init__(self, func):
        self.func = func
        self.cache = {}
    
    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]
    
    def clear_cache(self):
        self.cache = {}

@Memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(10))  # Uses cached values
```

### Context Decorator
```python
from contextlib import contextmanager

@contextmanager
def timer():
    """Context manager that times code execution"""
    from time import time
    start = time()
    yield
    end = time()
    print(f"Execution took {end - start:.2f} seconds")

# Use as context manager
with timer():
    # Some code
    import time
    time.sleep(1)

# Use as decorator
@timer()
def slow_function():
    import time
    time.sleep(1)
```

## Best Practices

### Using functools.wraps
```python
from functools import wraps

def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper  # Loses function metadata

def good_decorator(func):
    @wraps(func)  # Preserves function metadata
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def example():
    """This docstring is preserved"""
    pass

print(example.__name__)      # "example"
print(example.__doc__)       # "This docstring is preserved"
```

### Error Handling in Decorators
```python
def safe_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error in {func.__name__}: {str(e)}")
            return None
    return wrapper

@safe_call
def divide(a, b):
    return a / b

result = divide(10, 0)  # Handles ZeroDivisionError gracefully
```

## Practical Examples

```python
# 1. Rate limiting decorator
from time import time, sleep

def rate_limit(calls_per_second):
    min_interval = 1.0 / calls_per_second
    last_call_time = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time()
            if func in last_call_time:
                elapsed = current_time - last_call_time[func]
                if elapsed < min_interval:
                    sleep(min_interval - elapsed)
            
            result = func(*args, **kwargs)
            last_call_time[func] = time()
            return result
        return wrapper
    return decorator

# 2. Retry decorator
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    sleep(delay)
            return None
        return wrapper
    return decorator
```

## Exercises

1. Create a decorator that caches function results using a time-based expiration
2. Implement a decorator that logs function arguments and return values
3. Create a decorator that enforces type hints at runtime
4. Implement a decorator that measures and records function execution times
5. Create a decorator that implements the observer pattern for function calls