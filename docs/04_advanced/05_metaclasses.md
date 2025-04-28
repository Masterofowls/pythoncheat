# Python Metaclasses

## Basic Metaclasses

### Metaclass Syntax
```python
class MyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # Customize class creation
        return super().__new__(cls, name, bases, attrs)

class MyClass(metaclass=MyMetaclass):
    pass
```

### Custom Class Creation
```python
class LoggedMetaclass(type):
    def __new__(cls, name, bases, attrs):
        print(f"Creating class: {name}")
        print(f"Bases: {bases}")
        print(f"Attributes: {attrs}")
        return super().__new__(cls, name, bases, attrs)

class Example(metaclass=LoggedMetaclass):
    x = 1
    
    def method(self):
        pass
```

## Attribute Control

### Attribute Validation
```python
class ValidateAttributes(type):
    def __new__(cls, name, bases, attrs):
        # Check for required attributes
        required = {"name", "age"}
        for attr in required:
            if attr not in attrs:
                raise TypeError(f"Missing required attribute: {attr}")
        
        return super().__new__(cls, name, bases, attrs)

class Person(metaclass=ValidateAttributes):
    name = "John"
    age = 30
```

### Attribute Transformation
```python
class UpperAttributeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        uppercase_attrs = {
            key.upper(): value
            for key, value in attrs.items()
            if not key.startswith("__")
        }
        
        # Update with uppercase keys
        attrs.update(uppercase_attrs)
        return super().__new__(cls, name, bases, attrs)

class Config(metaclass=UpperAttributeMetaclass):
    host = "localhost"
    port = 8080
    
# Access with uppercase
print(Config.HOST)  # "localhost"
```

## Registry Pattern

### Class Registry
```python
class RegisteredMeta(type):
    _registry = {}
    
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        cls._registry[name] = new_cls
        return new_cls
    
    @classmethod
    def get_registry(cls):
        return dict(cls._registry)

class Registered(metaclass=RegisteredMeta):
    pass

class MyClass(Registered):
    pass

class AnotherClass(Registered):
    pass

# Access registry
print(RegisteredMeta.get_registry())
```

### Plugin System
```python
class PluginMeta(type):
    plugins = {}
    
    def __new__(cls, name, bases, attrs):
        new_cls = super().__new__(cls, name, bases, attrs)
        if "plugin_name" in attrs:
            cls.plugins[attrs["plugin_name"]] = new_cls
        return new_cls

class Plugin(metaclass=PluginMeta):
    @classmethod
    def get_plugin(cls, name):
        return cls.plugins.get(name)

class TextPlugin(Plugin):
    plugin_name = "text"
    
    def process(self, data):
        return data.upper()

class JSONPlugin(Plugin):
    plugin_name = "json"
    
    def process(self, data):
        import json
        return json.loads(data)
```

## Abstract Base Classes

### Custom ABC Implementation
```python
class ABCMeta(type):
    def __new__(cls, name, bases, attrs):
        for key, value in attrs.items():
            if getattr(value, "__isabstractmethod__", False):
                attrs[key] = property(value)
        return super().__new__(cls, name, bases, attrs)

class AbstractClass(metaclass=ABCMeta):
    @property
    def my_abstract_method(self):
        raise NotImplementedError

class ConcreteClass(AbstractClass):
    @property
    def my_abstract_method(self):
        return "Implemented"
```

### Interface Definition
```python
class InterfaceMeta(type):
    def __new__(cls, name, bases, attrs):
        # Verify interface implementation
        for key, value in attrs.items():
            if getattr(value, "__isabstractmethod__", False):
                raise TypeError(
                    f"Cannot create abstract class {name} with abstract "
                    f"method {key}"
                )
        return super().__new__(cls, name, bases, attrs)

class Interface(metaclass=InterfaceMeta):
    pass

class MyInterface(Interface):
    def method(self):
        pass
```

## Singleton Pattern

### Singleton Metaclass
```python
class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=Singleton):
    def __init__(self):
        self.connected = False
    
    def connect(self):
        self.connected = True

# Usage
db1 = Database()
db2 = Database()
print(db1 is db2)  # True
```

## Advanced Features

### Method Wrapping
```python
class LoggedMeta(type):
    def __new__(cls, name, bases, attrs):
        # Wrap all methods with logging
        for key, value in attrs.items():
            if callable(value):
                attrs[key] = cls.log_call(value)
        return super().__new__(cls, name, bases, attrs)
    
    @staticmethod
    def log_call(func):
        def wrapper(*args, **kwargs):
            print(f"Calling: {func.__name__}")
            result = func(*args, **kwargs)
            print(f"Finished: {func.__name__}")
            return result
        return wrapper

class MyClass(metaclass=LoggedMeta):
    def my_method(self):
        print("Method executing")
```

### Dynamic Attribute Creation
```python
class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        # Add getters and setters for attributes
        for key, value in list(attrs.items()):
            if not key.startswith("_"):
                attrs[f"get_{key}"] = lambda self, k=key: getattr(self, k)
                attrs[f"set_{key}"] = lambda self, v, k=key: setattr(self, k, v)
        return super().__new__(cls, name, bases, attrs)

class Model(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

class User(Model):
    name = None
    age = None
```

## Best Practices

### Error Handling
```python
class SafeMeta(type):
    def __new__(cls, name, bases, attrs):
        try:
            return super().__new__(cls, name, bases, attrs)
        except Exception as e:
            print(f"Error creating class {name}: {e}")
            return None

class MyClass(metaclass=SafeMeta):
    # This will handle errors during class creation
    pass
```

### Metaclass Composition
```python
class MetaA(type):
    def __new__(cls, name, bases, attrs):
        attrs["a"] = 1
        return super().__new__(cls, name, bases, attrs)

class MetaB(type):
    def __new__(cls, name, bases, attrs):
        attrs["b"] = 2
        return super().__new__(cls, name, bases, attrs)

class MetaC(MetaA, MetaB):
    pass

class MyClass(metaclass=MetaC):
    pass

# Access
print(MyClass.a)  # 1
print(MyClass.b)  # 2
```

## Exercises

1. Create a metaclass that automatically adds property decorators
2. Implement a metaclass for class-level dependency injection
3. Build a metaclass that enforces method naming conventions
4. Create a metaclass for automatic serialization/deserialization
5. Implement a metaclass that adds observer pattern functionality