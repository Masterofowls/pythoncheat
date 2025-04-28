# Python Decorators

## Basic Decorators

### Function Decorators
```python
def timer(func):
    """A decorator that prints the execution time of a function"""
    from time import time
    
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__} took {end - start:.2f} seconds")
        return result
    
    return wrapper

@timer
def slow_function():
    from time import sleep
    sleep(1)
    return "Done!"
```

### Multiple Decorators
```python
def bold(func):
    def wrapper():
        return f"<b>{func()}</b>"
    return wrapper

def italic(func):
    def wrapper():
        return f"<i>{func()}</i>"
    return wrapper

@bold
@italic
def greet():
    return "Hello!"

# Equivalent to: bold(italic(greet))()
print(greet())  # <b><i>Hello!</i></b>
```

## Decorators with Arguments

### Basic Parameterized Decorators
```python
def repeat(times):
    """Decorator that repeats a function call n times"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            results = []
            for _ in range(times):
                results.append(func(*args, **kwargs))
            return results
        return wrapper
    return decorator

@repeat(times=3)
def greet(name):
    return f"Hello {name}"

print(greet("Alice"))  # ['Hello Alice', 'Hello Alice', 'Hello Alice']
```

### Decorator Factory
```python
def log_to(filename):
    """Factory function that creates logging decorators"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'a') as f:
                f.write(f"{func.__name__} was called with result {result}\n")
            return result
        return wrapper
    return decorator

@log_to("debug.log")
def calculate(x, y):
    return x + y
```

## Class Decorators

### Basic Class Decorator
```python
def singleton(cls):
    """Decorator to convert a class into a singleton"""
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class Database:
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True
```

### Class Decorator with Parameters
```python
def validate_attributes(**validators):
    """Decorator that adds attribute validation to a class"""
    def decorator(cls):
        original_init = cls.__init__
        
        def __init__(self, *args, **kwargs):
            for key, validator in validators.items():
                if key in kwargs:
                    if not validator(kwargs[key]):
                        raise ValueError(f"Invalid value for {key}")
            original_init(self, *args, **kwargs)
        
        cls.__init__ = __init__
        return cls
    
    return decorator

@validate_attributes(age=lambda x: 0 <= x <= 150)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

## Method Decorators

### Property Decorator
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

### Class Method Decorator
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_string):
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        import datetime
        d = datetime.datetime.now()
        return cls(d.year, d.month, d.day)
```

## Advanced Decorator Patterns

### Decorator with State
```python
class CountCalls:
    """Decorator that counts function calls"""
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)
    
    def reset_count(self):
        self.count = 0

@CountCalls
def hello():
    return "Hello!"

hello()
print(hello.count)  # 1
```

### Decorator with Context Manager
```python
from contextlib import contextmanager

@contextmanager
def timer():
    """Context manager that times a block of code"""
    from time import time
    start = time()
    yield
    end = time()
    print(f"Elapsed time: {end - start:.2f} seconds")

def timing_decorator(func):
    def wrapper(*args, **kwargs):
        with timer():
            return func(*args, **kwargs)
    return wrapper

@timing_decorator
def slow_operation():
    from time import sleep
    sleep(1)
```

## Real-World Examples

### Caching Decorator
```python
def memoize(func):
    """Decorator that caches function results"""
    cache = {}
    
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    
    wrapper.cache = cache
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

### Retry Decorator
```python
def retry(max_attempts=3, delay=1):
    """Decorator that retries a function on failure"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    from time import sleep
                    sleep(delay)
            return None
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def unstable_network_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Network error")
    return "Success!"
```

### Authentication Decorator
```python
def require_auth(role=None):
    """Decorator that requires authentication"""
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if not hasattr(request, 'user'):
                raise ValueError("No user authenticated")
            
            if role and request.user.role != role:
                raise ValueError(f"User must have role: {role}")
            
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

class Request:
    def __init__(self, user):
        self.user = user

@require_auth(role='admin')
def sensitive_operation(request):
    return "Access granted!"
```

## Best Practices

### Preserving Function Metadata
```python
from functools import wraps

def decorator(func):
    @wraps(func)  # Preserves func's metadata
    def wrapper(*args, **kwargs):
        """Wrapper docstring"""
        return func(*args, **kwargs)
    return wrapper

@decorator
def greet(name):
    """Greet someone"""
    return f"Hello {name}"

print(greet.__name__)      # 'greet' (not 'wrapper')
print(greet.__doc__)       # 'Greet someone'
```

### Decorator Classes vs Functions
```python
# Class-based decorator (with state)
class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0
    
    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)

# Function-based decorator (stateless)
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

## Exercises

1. Create a decorator that measures and logs function execution time
2. Implement a caching decorator with a maximum cache size
3. Build a decorator that validates function arguments
4. Create a decorator that implements retry logic with exponential backoff
5. Implement a decorator that adds rate limiting to a function