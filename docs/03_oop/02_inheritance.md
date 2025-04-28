# Python Inheritance

## Basic Inheritance

### Single Inheritance
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# Usage
dog = Dog("Rex")
print(dog.speak())  # Rex says Woof!
```

### Method Override
```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand
    
    def start(self):
        return "Vehicle starting..."
    
    def stop(self):
        return "Vehicle stopping..."

class Car(Vehicle):
    def start(self):
        return f"{self.brand} car engine starting..."
    
    def stop(self):
        return f"{self.brand} car engine stopping..."
```

## Multiple Inheritance

### Basic Multiple Inheritance
```python
class Flying:
    def fly(self):
        return "Flying high!"

class Swimming:
    def swim(self):
        return "Swimming deep!"

class Duck(Flying, Swimming):
    def __init__(self, name):
        self.name = name
    
    def move(self):
        return f"{self.name} can {self.fly()} and {self.swim()}"

# Usage
donald = Duck("Donald")
print(donald.move())
```

### Method Resolution Order (MRO)
```python
class A:
    def method(self):
        return "A method"

class B(A):
    def method(self):
        return "B method"

class C(A):
    def method(self):
        return "C method"

class D(B, C):
    pass

# Check MRO
print(D.__mro__)  
# (<class '__main__.D'>, <class '__main__.B'>, 
#  <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)
```

## Super() Function

### Basic Super Usage
```python
class Animal:
    def __init__(self, name):
        self.name = name

class Pet(Animal):
    def __init__(self, name, owner):
        super().__init__(name)
        self.owner = owner

# Multiple Inheritance with super()
class Bird:
    def __init__(self, can_fly=True):
        self.can_fly = can_fly

class Parrot(Pet, Bird):
    def __init__(self, name, owner):
        Pet.__init__(self, name, owner)
        Bird.__init__(self)
```

### Super with Multiple Inheritance
```python
class A:
    def method(self):
        print("A method")

class B(A):
    def method(self):
        super().method()
        print("B method")

class C(A):
    def method(self):
        super().method()
        print("C method")

class D(B, C):
    def method(self):
        super().method()
        print("D method")
```

## Abstract Base Classes

### Basic Abstract Class
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
```

### Abstract Properties
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def wheel_count(self):
        pass
    
    @abstractmethod
    def start_engine(self):
        pass

class Car(Vehicle):
    @property
    def wheel_count(self):
        return 4
    
    def start_engine(self):
        return "Car engine starting..."
```

## Mixins

### Feature Mixins
```python
class JSONSerializableMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggerMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class User(JSONSerializableMixin, LoggerMixin):
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

### Utility Mixins
```python
class PrintableMixin:
    def print_info(self):
        for key, value in self.__dict__.items():
            print(f"{key}: {value}")

class ValidatorMixin:
    def validate_age(self, age):
        if not isinstance(age, int) or age < 0:
            raise ValueError("Age must be a positive integer")

class Person(PrintableMixin, ValidatorMixin):
    def __init__(self, name, age):
        self.validate_age(age)
        self.name = name
        self.age = age
```

## Best Practices

### Inheritance vs Composition
```python
# Inheritance - "is-a" relationship
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    pass

# Composition - "has-a" relationship
class Engine:
    def start(self):
        return "Engine starting..."

class Car:
    def __init__(self):
        self.engine = Engine()
    
    def start(self):
        return self.engine.start()
```

### Method Delegation
```python
class Stack:
    def __init__(self):
        self._items = []
    
    def __getattr__(self, name):
        # Delegate unknown attributes to internal list
        return getattr(self._items, name)
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        return self._items.pop()
```

## Common Patterns

### Template Method Pattern
```python
class DataMiner(ABC):
    def mine(self):
        self.open_file()
        self.extract_data()
        self.parse_data()
        self.close_file()
    
    @abstractmethod
    def open_file(self):
        pass
    
    @abstractmethod
    def extract_data(self):
        pass
    
    @abstractmethod
    def parse_data(self):
        pass
    
    def close_file(self):
        print("Closing file")

class PDFDataMiner(DataMiner):
    def open_file(self):
        print("Opening PDF file")
    
    def extract_data(self):
        print("Extracting PDF data")
    
    def parse_data(self):
        print("Parsing PDF data")
```

### Factory Method Pattern
```python
class Creator(ABC):
    @abstractmethod
    def factory_method(self):
        pass
    
    def operation(self):
        product = self.factory_method()
        return product.operation()

class ConcreteCreator1(Creator):
    def factory_method(self):
        return ConcreteProduct1()

class Product(ABC):
    @abstractmethod
    def operation(self):
        pass

class ConcreteProduct1(Product):
    def operation(self):
        return "Result of ConcreteProduct1"
```

## Exercises

1. Create a hierarchy of shapes with abstract base class and concrete implementations
2. Implement a logging system using mixins and inheritance
3. Build a file processing system using template method pattern
4. Create a class hierarchy for different types of vehicles
5. Implement a plugin system using inheritance and abstract base classes