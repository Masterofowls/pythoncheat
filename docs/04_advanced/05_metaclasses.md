# Python Metaclasses

## Basic Metaclasses

### Creating Metaclasses
```python
class MyMetaclass(type):
    """Simple metaclass example"""
    def __new__(cls, name, bases, attrs):
        # Add a new method to the class
        attrs['custom_method'] = lambda self: f"Custom method in {name}"
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MyMetaclass):
    def normal_method(self):
        return "Normal method"

# Using the class
obj = MyClass()
print(obj.normal_method())    # Normal method
print(obj.custom_method())    # Custom method in MyClass
```

### Class Creation Control
```python
class ValidateMeta(type):
    """Metaclass that validates class attributes"""
    def __new__(cls, name, bases, attrs):
        # Check for required attributes
        required = {'name', 'age'}
        missing = required - set(attrs)
        if missing:
            raise TypeError(f"Missing required attributes: {missing}")
        
        # Validate attribute types
        if not isinstance(attrs.get('name'), str):
            raise TypeError("name must be a string")
        if not isinstance(attrs.get('age'), int):
            raise TypeError("age must be an integer")
        
        return super().__new__(cls, name, bases, attrs)

class Person(metaclass=ValidateMeta):
    name = "John"
    age = 30

# This would raise TypeError:
# class InvalidPerson(metaclass=ValidateMeta):
#     name = 123  # Wrong type
#     age = "30"  # Wrong type
```

## Advanced Metaclass Features

### Attribute Transformation
```python
class UpperAttributesMeta(type):
    """Metaclass that converts all string attributes to uppercase"""
    def __new__(cls, name, bases, attrs):
        uppercase_attrs = {
            key: value.upper() if isinstance(value, str) else value
            for key, value in attrs.items()
        }
        return super().__new__(cls, name, bases, uppercase_attrs)

class Config(metaclass=UpperAttributesMeta):
    host = "localhost"
    port = 8080
    username = "admin"

print(Config.host)      # LOCALHOST
print(Config.username)  # ADMIN
print(Config.port)      # 8080 (unchanged)
```

### Method Wrapping
```python
from functools import wraps
import time

class TimingMeta(type):
    """Metaclass that adds timing to all methods"""
    def __new__(cls, name, bases, attrs):
        # Wrap all methods with timing functionality
        for attr_name, attr_value in attrs.items():
            if callable(attr_value):
                attrs[attr_name] = cls.time_method(attr_value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def time_method(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            print(f"{method.__name__} took {end - start:.2f} seconds")
            return result
        return wrapper

class Operations(metaclass=TimingMeta):
    def slow_operation(self):
        time.sleep(1)
        return "Done"

# All methods are automatically timed
ops = Operations()
ops.slow_operation()  # prints timing information
```

### Registry Pattern
```python
class RegisteredMeta(type):
    """Metaclass that maintains a registry of all subclasses"""
    _registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        cls._registry[name] = new_cls
        return new_cls
    
    @classmethod
    def get_registry(cls):
        return dict(cls._registry)

class Plugin(metaclass=RegisteredMeta):
    """Base class for plugins"""
    pass

class AudioPlugin(Plugin):
    """Audio processing plugin"""
    pass

class VideoPlugin(Plugin):
    """Video processing plugin"""
    pass

# Access registry
plugins = RegisteredMeta.get_registry()
print(plugins)  # {'Plugin': <class 'Plugin'>, 'AudioPlugin': <class 'AudioPlugin'>, ...}
```

## Advanced Applications

### Abstract Base Class Creation
```python
class InterfaceMeta(type):
    """Metaclass for creating interfaces"""
    def __new__(cls, name, bases, attrs):
        # Check for abstract method implementations
        for key, value in attrs.items():
            if getattr(value, "__isabstractmethod__", False):
                continue
            if key.startswith('_'):
                continue
            if not callable(value):
                continue
            # Mark public methods as abstract
            attrs[key].__isabstractmethod__ = True
        return super().__new__(cls, name, bases, attrs)

class Interface(metaclass=InterfaceMeta):
    """Base class for interfaces"""
    pass

class DataProvider(Interface):
    def get_data(self):
        """Must be implemented by subclasses"""
        pass
    
    def save_data(self, data):
        """Must be implemented by subclasses"""
        pass

# This would raise TypeError (can't instantiate abstract class):
# provider = DataProvider()
```

### Singleton Implementation
```python
class Singleton(type):
    """Metaclass for creating singleton classes"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        print("Initializing database connection")

# Only creates one instance
db1 = Database()  # Prints initialization message
db2 = Database()  # No message
print(db1 is db2)  # True
```

### Attribute Validation
```python
class ValidateAttributes(type):
    """Metaclass for attribute type validation"""
    @staticmethod
    def validate_type(name, value, expected_type):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be {expected_type}")
        return value
    
    def __new__(cls, name, bases, attrs):
        annotations = attrs.get('__annotations__', {})
        for key, value in attrs.items():
            if key in annotations:
                attrs[key] = cls.validate_type(
                    key, value, annotations[key]
                )
        return super().__new__(cls, name, bases, attrs)

class User(metaclass=ValidateAttributes):
    name: str = "John"
    age: int = 30
    active: bool = True

# This would raise TypeError:
# class InvalidUser(metaclass=ValidateAttributes):
#     name: str = 123  # Wrong type
```

## Best Practices

### Metaclass Inheritance
```python
class BaseMeta(type):
    """Base metaclass with common functionality"""
    def __new__(cls, name, bases, attrs):
        # Add creation timestamp
        attrs['created_at'] = time.time()
        return super().__new__(cls, name, bases, attrs)

class LoggedMeta(BaseMeta):
    """Metaclass that adds logging"""
    def __new__(cls, name, bases, attrs):
        # Add logging to methods
        for key, value in attrs.items():
            if callable(value):
                attrs[key] = cls.log_call(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def log_call(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            print(f"Calling {method.__name__}")
            return method(*args, **kwargs)
        return wrapper

class MyClass(metaclass=LoggedMeta):
    def some_method(self):
        return "Method called"
```

### Error Handling
```python
class SafeMeta(type):
    """Metaclass with error handling"""
    def __new__(cls, name, bases, attrs):
        try:
            # Wrap all methods with error handling
            for key, value in attrs.items():
                if callable(value):
                    attrs[key] = cls.handle_errors(value)
            return super().__new__(cls, name, bases, attrs)
        except Exception as e:
            print(f"Error creating class {name}: {e}")
            raise
    
    @staticmethod
    def handle_errors(method):
        @wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except Exception as e:
                print(f"Error in {method.__name__}: {e}")
                return None
        return wrapper
```

## Common Patterns

### Factory Pattern
```python
class FactoryMeta(type):
    """Metaclass for implementing factory pattern"""
    def __call__(cls, product_type, *args, **kwargs):
        if not hasattr(cls, f'create_{product_type}'):
            raise ValueError(f"Unknown product type: {product_type}")
        creator = getattr(cls, f'create_{product_type}')
        return creator(*args, **kwargs)

class ProductFactory(metaclass=FactoryMeta):
    @staticmethod
    def create_book(title, author):
        return {'type': 'book', 'title': title, 'author': author}
    
    @staticmethod
    def create_movie(title, director):
        return {'type': 'movie', 'title': title, 'director': director}

# Using the factory
book = ProductFactory('book', 'Python 101', 'John Doe')
movie = ProductFactory('movie', 'Python: The Movie', 'Jane Smith')
```

## Exercises

1. Create a metaclass that automatically adds property getters and setters
2. Implement a metaclass for automatic serialization/deserialization
3. Create a metaclass that enforces method naming conventions
4. Implement a metaclass for managing database table schemas
5. Create a metaclass that adds debugging capabilities to all methods