# Python Descriptors

## Basic Descriptors

### Descriptor Protocol
```python
class Descriptor:
    """Basic descriptor implementation"""
    def __init__(self, initial_value=None):
        self.value = initial_value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value
    
    def __set__(self, instance, value):
        self.value = value
    
    def __delete__(self, instance):
        del self.value

class Example:
    x = Descriptor(1)

# Using descriptors
obj = Example()
print(obj.x)      # 1
obj.x = 2
print(obj.x)      # 2
```

### Data Descriptors
```python
class TypedDescriptor:
    """Descriptor that enforces type checking"""
    def __init__(self, type_):
        self.type = type_
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self._name)
    
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f"{self._name} must be of type {self.type}")
        instance.__dict__[self._name] = value

class Person:
    name = TypedDescriptor(str)
    age = TypedDescriptor(int)
    
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

## Property Descriptors

### Property Implementation
```python
class Property:
    """Custom implementation of the property descriptor"""
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(instance)
    
    def __set__(self, instance, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance, value)
    
    def __delete__(self, instance):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(instance)
    
    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)
    
    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)
    
    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @Property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
```

## Validation Descriptors

### Type Validation
```python
class Typed:
    """Descriptor for type validation"""
    def __init__(self, type_):
        self.type = type_
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]
    
    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f'{self._name} must be a {self.type}')
        instance.__dict__[self._name] = value

class Integer(Typed):
    def __init__(self):
        super().__init__(int)

class String(Typed):
    def __init__(self):
        super().__init__(str)

class Float(Typed):
    def __init__(self):
        super().__init__(float)

class Point:
    x = Float()
    y = Float()
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
```

### Range Validation
```python
class Positive:
    """Descriptor that ensures value is positive"""
    def __init__(self):
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]
    
    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError(f'{self._name} must be positive')
        instance.__dict__[self._name] = value

class Range:
    """Descriptor for range validation"""
    def __init__(self, min_val=None, max_val=None):
        self.min_val = min_val
        self.max_val = max_val
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self._name]
    
    def __set__(self, instance, value):
        if self.min_val is not None and value < self.min_val:
            raise ValueError(f'{self._name} must be ≥ {self.min_val}')
        if self.max_val is not None and value > self.max_val:
            raise ValueError(f'{self._name} must be ≤ {self.max_val}')
        instance.__dict__[self._name] = value
```

## Computed Attributes

### Lazy Properties
```python
class LazyProperty:
    """Descriptor for lazy-loaded attributes"""
    def __init__(self, func):
        self.func = func
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        value = self.func(instance)
        # Cache the computed value
        instance.__dict__[self._name] = value
        return value

class DataProcessor:
    def __init__(self, filename):
        self.filename = filename
    
    @LazyProperty
    def data(self):
        print("Loading data...")
        with open(self.filename) as f:
            return f.read()
```

### Cached Properties
```python
class CachedProperty:
    """Descriptor that caches computed values"""
    def __init__(self, func):
        self.func = func
        self._name = None
    
    def __set_name__(self, owner, name):
        self._name = name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        
        cache_name = f'_cached_{self._name}'
        if not hasattr(instance, cache_name):
            setattr(instance, cache_name, self.func(instance))
        return getattr(instance, cache_name)
    
    def __delete__(self, instance):
        cache_name = f'_cached_{self._name}'
        if hasattr(instance, cache_name):
            delattr(instance, cache_name)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    @CachedProperty
    def area(self):
        print("Computing area...")
        return 3.14159 * self.radius ** 2
```

## Best Practices

### Memory Management
```python
class WeakrefDescriptor:
    """Descriptor that uses weak references"""
    def __init__(self):
        self._values = weakref.WeakKeyDictionary()
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)
    
    def __set__(self, instance, value):
        self._values[instance] = value

class Cache:
    data = WeakrefDescriptor()
```

### Descriptor Factory
```python
def validated(type_, min_val=None, max_val=None):
    """Factory function for creating validated descriptors"""
    class Validator:
        def __init__(self):
            self._name = None
        
        def __set_name__(self, owner, name):
            self._name = name
        
        def __get__(self, instance, owner):
            if instance is None:
                return self
            return instance.__dict__.get(self._name)
        
        def __set__(self, instance, value):
            if not isinstance(value, type_):
                raise TypeError(f'{self._name} must be a {type_}')
            if min_val is not None and value < min_val:
                raise ValueError(f'{self._name} must be ≥ {min_val}')
            if max_val is not None and value > max_val:
                raise ValueError(f'{self._name} must be ≤ {max_val}')
            instance.__dict__[self._name] = value
    
    return Validator()

class Person:
    age = validated(int, 0, 150)
    height = validated(float, 0)
```

## Exercises

1. Create a descriptor that validates email addresses
2. Implement a descriptor for logging attribute access
3. Build a descriptor that implements unit conversion
4. Create a descriptor for managing database fields
5. Implement a descriptor that supports default values