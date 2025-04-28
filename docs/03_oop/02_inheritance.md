# Python Inheritance

## Basic Inheritance

### Single Inheritance
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def introduce(self):
        return f"I am {self.name}"

class Dog(Animal):
    def speak(self):
        return "Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball"

# Using inheritance
dog = Dog("Rex")
print(dog.introduce())  # I am Rex
print(dog.speak())      # Woof!
print(dog.fetch())      # Rex is fetching the ball
```

### Method Override
```python
class Bird(Animal):
    def __init__(self, name, wingspan):
        super().__init__(name)  # Call parent's __init__
        self.wingspan = wingspan
    
    def speak(self):
        return "Tweet!"
    
    def introduce(self):
        base_intro = super().introduce()
        return f"{base_intro} and I have a wingspan of {self.wingspan}cm"

bird = Bird("Polly", 20)
print(bird.introduce())  # I am Polly and I have a wingspan of 20cm
```

## Multiple Inheritance

### Basic Multiple Inheritance
```python
class Flyable:
    def fly(self):
        return "I can fly!"
    
    def land(self):
        return "Landing..."

class Swimmable:
    def swim(self):
        return "I can swim!"
    
    def dive(self):
        return "Diving..."

class Duck(Animal, Flyable, Swimmable):
    def speak(self):
        return "Quack!"

# Using multiple inheritance
duck = Duck("Donald")
print(duck.speak())   # Quack!
print(duck.fly())     # I can fly!
print(duck.swim())    # I can swim!
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

# Understanding MRO
print(D.__mro__)  # Method resolution order
# (<class '__main__.D'>, <class '__main__.B'>, 
#  <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

d = D()
print(d.method())  # B method (first in MRO)
```

## Abstract Base Classes

### Using ABC Module
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def describe(self):
        return f"Area: {self.area()}, Perimeter: {self.perimeter()}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# Cannot instantiate abstract class
# shape = Shape()  # TypeError
rect = Rectangle(5, 3)
print(rect.describe())  # Area: 15, Perimeter: 16
```

### Abstract Properties
```python
class Vehicle(ABC):
    def __init__(self, model):
        self._model = model
    
    @property
    @abstractmethod
    def vehicle_type(self):
        pass
    
    @property
    def model(self):
        return self._model

class Car(Vehicle):
    @property
    def vehicle_type(self):
        return "Car"

car = Car("Toyota")
print(car.vehicle_type)  # Car
```

## Interface Implementation

### Informal Interfaces
```python
class Drawable:
    def draw(self):
        raise NotImplementedError
    
    def get_bounds(self):
        raise NotImplementedError

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self):
        return f"Drawing Circle at ({self.x}, {self.y}) with radius {self.radius}"
    
    def get_bounds(self):
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )
```

### Protocol Classes (Python 3.8+)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def get_bounds(self) -> tuple: ...

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self) -> str:
        return f"Drawing Rectangle at ({self.x}, {self.y})"
    
    def get_bounds(self) -> tuple:
        return (self.x, self.y, self.x + self.width, self.y + self.height)

# Type checking
def draw_shape(shape: Drawable):
    print(shape.draw())

rect = Rectangle(0, 0, 10, 10)
draw_shape(rect)  # Valid
```

## Mixins

### Feature Mixins
```python
class JSONSerializerMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class LoggerMixin:
    def log(self, message):
        print(f"[{self.__class__.__name__}] {message}")

class User(JSONSerializerMixin, LoggerMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save(self):
        self.log(f"Saving user {self.name}")
        json_data = self.to_json()
        # Save to database...

user = User("Alice", "alice@email.com")
user.save()
print(user.to_json())
```

### Composable Mixins
```python
class ValidatorMixin:
    def validate(self):
        for field in self.required_fields:
            if not hasattr(self, field):
                raise ValueError(f"Missing required field: {field}")

class TimestampMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from datetime import datetime
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def update(self):
        self.updated_at = datetime.now()

class Post(ValidatorMixin, TimestampMixin):
    required_fields = ['title', 'content']
    
    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content
```

## Best Practices

### Composition vs Inheritance
```python
# Inheritance - "is-a" relationship
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def bark(self):
        return "Woof!"

# Composition - "has-a" relationship
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()
    
    def start(self):
        return self.engine.start()
```

### Dependency Injection
```python
class Database:
    def save(self, data):
        pass

class FileSystem:
    def save(self, data):
        pass

class UserService:
    def __init__(self, storage):
        self.storage = storage
    
    def save_user(self, user_data):
        return self.storage.save(user_data)

# Using different storage methods
db_service = UserService(Database())
file_service = UserService(FileSystem())
```

## Common Patterns

### Template Method Pattern
```python
class DataMiner(ABC):
    def mine(self):
        self.open_file()
        self.extract_data()
        self.parse_data()
        self.analyze_data()
        self.send_report()
        self.close_file()
    
    @abstractmethod
    def extract_data(self):
        pass
    
    @abstractmethod
    def analyze_data(self):
        pass

class PDFDataMiner(DataMiner):
    def extract_data(self):
        print("Extracting PDF data")
    
    def analyze_data(self):
        print("Analyzing PDF data")
```

### Strategy Pattern
```python
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data):
        pass

class QuickSort(SortStrategy):
    def sort(self, data):
        # Implementation
        return sorted(data)

class MergeSort(SortStrategy):
    def sort(self, data):
        # Implementation
        return sorted(data)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy
    
    def sort(self, data):
        return self.strategy.sort(data)
```

## Practice Examples

```python
# 1. Shape hierarchy with multiple inheritance
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Colorable:
    def __init__(self, color):
        self.color = color
    
    def get_color(self):
        return self.color

class ColoredCircle(Shape, Colorable):
    def __init__(self, radius, color):
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2

# 2. Plugin system using inheritance
class Plugin(ABC):
    @abstractmethod
    def activate(self):
        pass
    
    @abstractmethod
    def deactivate(self):
        pass

class ImagePlugin(Plugin):
    def activate(self):
        print("Image plugin activated")
    
    def deactivate(self):
        print("Image plugin deactivated")
```

## Exercises

1. Create a vehicle hierarchy with different types of vehicles and shared behaviors
2. Implement a simple plugin system using abstract base classes
3. Design a shape system using multiple inheritance for different features (color, texture, etc.)
4. Create a logging system using mixins for different output formats
5. Implement a payment processing system using the Strategy pattern and inheritance