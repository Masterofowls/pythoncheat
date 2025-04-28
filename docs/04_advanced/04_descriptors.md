# Python Descriptors

## Basic Descriptors

### Descriptor Protocol
```python
class DescriptorExample:
    """Basic descriptor implementation"""
    def __init__(self, name=None):
        self.name = name
    
    def __get__(self, instance, owner):
        """Get value from descriptor"""
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        """Set value in descriptor"""
        instance.__dict__[self.name] = value
    
    def __delete__(self, instance):
        """Delete value from descriptor"""
        del instance.__dict__[self.name]

class Person:
    name = DescriptorExample('name')
    
    def __init__(self, name):
        self.name = name

# Using descriptors
person = Person("Alice")
print(person.name)  # Alice
```

### Data Descriptors
```python
class Validated:
    """Data descriptor with validation"""
    def __init__(self, minvalue=None, maxvalue=None):
        self.minvalue = minvalue
        self.maxvalue = maxvalue
        self.name = None
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.minvalue is not None and value < self.minvalue:
            raise ValueError(f"Value must be ≥ {self.minvalue}")
        if self.maxvalue is not None and value > self.maxvalue:
            raise ValueError(f"Value must be ≤ {self.maxvalue}")
        instance.__dict__[self.name] = value
    
    def __set_name__(self, owner, name):
        self.name = name

class Product:
    price = Validated(minvalue=0)
    quantity = Validated(minvalue=0, maxvalue=100)
    
    def __init__(self, price, quantity):
        self.price = price
        self.quantity = quantity
```

### Non-Data Descriptors
```python
class LazyProperty:
    """Non-data descriptor for lazy property computation"""
    def __init__(self, function):
        self.function = function
        self.name = function.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        # Compute value and store in instance dict
        value = self.function(instance)
        instance.__dict__[self.name] = value
        return value

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @LazyProperty
    def area(self):
        print("Computing area...")
        return 3.14159 * self.radius ** 2

# Using lazy property
circle = Circle(5)
print(circle.area)  # Computes first time
print(circle.area)  # Uses cached value
```

## Advanced Descriptors

### Property Factory
```python
def typed_property(name, expected_type):
    """Create a property with type checking"""
    storage_name = f'_{name}'
    
    @property
    def prop(self):
        return getattr(self, storage_name)
    
    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be a {expected_type}")
        setattr(self, storage_name, value)
    
    return prop

class Person:
    name = typed_property("name", str)
    age = typed_property("age", int)
    
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age

# Using typed properties
person = Person("Alice", 30)
# person.age = "30"  # TypeError: age must be a <class 'int'>
```

### Descriptor with History
```python
class HistoryDescriptor:
    """Descriptor that maintains history of values"""
    def __init__(self):
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        history = instance.__dict__.get(f'_{self.name}_history', [])
        return history[-1] if history else None
    
    def __set__(self, instance, value):
        history_name = f'_{self.name}_history'
        if history_name not in instance.__dict__:
            instance.__dict__[history_name] = []
        instance.__dict__[history_name].append(value)

class TrackedPerson:
    name = HistoryDescriptor()
    
    def get_name_history(self):
        return getattr(self, '_name_history', [])

# Using history tracking
person = TrackedPerson()
person.name = "Alice"
person.name = "Alicia"
print(person.get_name_history())  # ['Alice', 'Alicia']
```

### Method Descriptors
```python
class MethodDescriptor:
    """Descriptor that can act as method or property"""
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return lambda *args, **kwargs: self.func(instance, *args, **kwargs)

class Calculator:
    @MethodDescriptor
    def add(self, x, y):
        return x + y
    
    @MethodDescriptor
    def multiply(self, x, y):
        return x * y

# Using method descriptor
calc = Calculator()
print(calc.add(2, 3))       # 5
print(calc.multiply(2, 3))  # 6
```

## Practical Applications

### Validation and Type Checking
```python
class Validated:
    """Generic validator descriptor"""
    def __init__(self, *validators):
        self.validators = validators
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        for validator in self.validators:
            validator(value)
        instance.__dict__[self.name] = value

# Validator functions
def positive(value):
    if value <= 0:
        raise ValueError("Value must be positive")

def max_length(length):
    def validate(value):
        if len(str(value)) > length:
            raise ValueError(f"Value must not exceed {length} characters")
    return validate

class Product:
    price = Validated(positive)
    name = Validated(max_length(50))
```

### Computed Properties
```python
class ComputedProperty:
    """Property that depends on other attributes"""
    def __init__(self, compute_func):
        self.compute_func = compute_func
        self.name = compute_func.__name__
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.compute_func(instance)

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    @ComputedProperty
    def area(self):
        return self.width * self.height
    
    @ComputedProperty
    def perimeter(self):
        return 2 * (self.width + self.height)
```

### Unit Conversion
```python
class Unit:
    """Descriptor for unit conversion"""
    def __init__(self, unit_type):
        self.unit_type = unit_type
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]
    
    def __set__(self, instance, value):
        if self.unit_type == "temperature":
            instance.__dict__[self.name] = value
            instance.__dict__[f"{self.name}_fahrenheit"] = (value * 9/5) + 32
        elif self.unit_type == "distance":
            instance.__dict__[self.name] = value
            instance.__dict__[f"{self.name}_feet"] = value * 3.28084

class Measurement:
    celsius = Unit("temperature")
    meters = Unit("distance")
    
    def __init__(self, celsius, meters):
        self.celsius = celsius
        self.meters = meters
```

## Best Practices

### Performance Considerations
```python
class CachedProperty:
    """Property with caching and optional timeout"""
    def __init__(self, func, timeout=None):
        self.func = func
        self.timeout = timeout
        self.name = func.__name__
        self.cache_name = f'_cached_{func.__name__}'
        self.timestamp_name = f'_timestamp_{func.__name__}'
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        now = time.time()
        if (self.cache_name in instance.__dict__ and
            (self.timeout is None or
             now - getattr(instance, self.timestamp_name, 0) < self.timeout)):
            return instance.__dict__[self.cache_name]
        
        value = self.func(instance)
        instance.__dict__[self.cache_name] = value
        if self.timeout is not None:
            instance.__dict__[self.timestamp_name] = now
        return value
```

### Error Handling
```python
class SafeDescriptor:
    """Descriptor with error handling"""
    def __init__(self, name=None, default=None):
        self.name = name
        self.default = default
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        try:
            return instance.__dict__.get(self.name, self.default)
        except Exception as e:
            print(f"Error accessing {self.name}: {e}")
            return self.default
    
    def __set__(self, instance, value):
        try:
            instance.__dict__[self.name] = value
        except Exception as e:
            print(f"Error setting {self.name}: {e}")
```

## Exercises

1. Create a descriptor for automatic data type conversion
2. Implement a descriptor that maintains an audit log of attribute changes
3. Create a descriptor for attribute value range validation
4. Implement a descriptor for lazy loading of expensive resources
5. Create a descriptor for managing database column mappings