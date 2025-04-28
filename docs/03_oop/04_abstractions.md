# Python Abstractions

## Abstract Base Classes (ABC)

### Basic Abstract Class
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """Calculate area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Calculate perimeter of the shape"""
        pass
    
    def describe(self) -> str:
        """Non-abstract method using abstract methods"""
        return f"Area: {self.area()}, Perimeter: {self.perimeter()}"

class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
```

### Abstract Properties
```python
class Vehicle(ABC):
    def __init__(self, model: str):
        self._model = model
    
    @property
    @abstractmethod
    def vehicle_type(self) -> str:
        """The type of vehicle"""
        pass
    
    @property
    @abstractmethod
    def fuel_capacity(self) -> float:
        """Fuel capacity in liters"""
        pass
    
    @property
    def model(self) -> str:
        return self._model

class Car(Vehicle):
    @property
    def vehicle_type(self) -> str:
        return "Car"
    
    @property
    def fuel_capacity(self) -> float:
        return 45.0  # Standard car fuel tank
```

## Interfaces

### Informal Interfaces
```python
class Serializable:
    """Interface for objects that can be serialized"""
    def serialize(self) -> dict:
        raise NotImplementedError
    
    def deserialize(self, data: dict) -> None:
        raise NotImplementedError

class JSONSerializable:
    """Interface for JSON serialization"""
    def to_json(self) -> str:
        raise NotImplementedError
    
    def from_json(self, json_str: str) -> None:
        raise NotImplementedError

class User(Serializable, JSONSerializable):
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
    
    def serialize(self) -> dict:
        return {"name": self.name, "age": self.age}
    
    def deserialize(self, data: dict) -> None:
        self.name = data["name"]
        self.age = data["age"]
    
    def to_json(self) -> str:
        import json
        return json.dumps(self.serialize())
    
    def from_json(self, json_str: str) -> None:
        import json
        self.deserialize(json.loads(json_str))
```

### Protocol Classes (Python 3.8+)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def get_bounds(self) -> tuple[float, float, float, float]: ...

@runtime_checkable
class Resizable(Protocol):
    def resize(self, factor: float) -> None: ...

class Circle:
    def __init__(self, x: float, y: float, radius: float):
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self) -> str:
        return f"Drawing Circle at ({self.x}, {self.y})"
    
    def get_bounds(self) -> tuple[float, float, float, float]:
        return (
            self.x - self.radius,
            self.y - self.radius,
            self.x + self.radius,
            self.y + self.radius
        )
    
    def resize(self, factor: float) -> None:
        self.radius *= factor

# Type checking
def draw_shape(shape: Drawable) -> None:
    print(shape.draw())

def resize_shape(shape: Resizable, factor: float) -> None:
    shape.resize(factor)
```

## Abstract Collections

### Abstract Container Types
```python
from collections.abc import Sequence, MutableSequence

class ReadOnlyList(Sequence):
    def __init__(self, data):
        self._data = list(data)
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, index):
        return self._data[index]

class EditableList(MutableSequence):
    def __init__(self):
        self._data = []
    
    def __len__(self):
        return len(self._data)
    
    def __getitem__(self, index):
        return self._data[index]
    
    def __setitem__(self, index, value):
        self._data[index] = value
    
    def __delitem__(self, index):
        del self._data[index]
    
    def insert(self, index, value):
        self._data.insert(index, value)
```

## Best Practices

### Interface Segregation
```python
# Bad: Too many methods in one interface
class AnimalInterface(ABC):
    @abstractmethod
    def walk(self): pass
    
    @abstractmethod
    def swim(self): pass
    
    @abstractmethod
    def fly(self): pass

# Good: Segregated interfaces
class Walker(Protocol):
    def walk(self) -> None: ...

class Swimmer(Protocol):
    def swim(self) -> None: ...

class Flyer(Protocol):
    def fly(self) -> None: ...

class Bird(Flyer, Walker):
    def walk(self) -> None:
        print("Walking...")
    
    def fly(self) -> None:
        print("Flying...")
```

### Dependency Inversion
```python
class DataStore(Protocol):
    def save(self, data: dict) -> None: ...
    def load(self) -> dict: ...

class FileStorage:
    def __init__(self, filename: str):
        self.filename = filename
    
    def save(self, data: dict) -> None:
        with open(self.filename, 'w') as f:
            json.dump(data, f)
    
    def load(self) -> dict:
        with open(self.filename, 'r') as f:
            return json.load(f)

class DatabaseStorage:
    def save(self, data: dict) -> None:
        # Save to database
        pass
    
    def load(self) -> dict:
        # Load from database
        pass

class UserManager:
    def __init__(self, storage: DataStore):
        self.storage = storage
    
    def save_user(self, user: dict) -> None:
        self.storage.save(user)
    
    def load_user(self) -> dict:
        return self.storage.load()
```

## Advanced Patterns

### Abstract Factory
```python
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> 'Button':
        pass
    
    @abstractmethod
    def create_window(self) -> 'Window':
        pass

class Button(ABC):
    @abstractmethod
    def paint(self) -> None:
        pass

class Window(ABC):
    @abstractmethod
    def render(self) -> None:
        pass

class WindowsFactory(GUIFactory):
    def create_button(self) -> 'WindowsButton':
        return WindowsButton()
    
    def create_window(self) -> 'WindowsWindow':
        return WindowsWindow()

class MacFactory(GUIFactory):
    def create_button(self) -> 'MacButton':
        return MacButton()
    
    def create_window(self) -> 'MacWindow':
        return MacWindow()
```

### Template Method
```python
class DataMiner(ABC):
    def mine(self) -> dict:
        data = self.extract()
        clean_data = self.transform(data)
        return self.load(clean_data)
    
    @abstractmethod
    def extract(self) -> list:
        """Extract data from source"""
        pass
    
    @abstractmethod
    def transform(self, data: list) -> list:
        """Clean and transform the data"""
        pass
    
    @abstractmethod
    def load(self, data: list) -> dict:
        """Load data into target format"""
        pass

class CSVDataMiner(DataMiner):
    def __init__(self, filename: str):
        self.filename = filename
    
    def extract(self) -> list:
        # Read from CSV
        pass
    
    def transform(self, data: list) -> list:
        # Clean CSV data
        pass
    
    def load(self, data: list) -> dict:
        # Convert to dict
        pass
```

## Common Design Patterns with Abstractions

### Observer Pattern
```python
class Observer(Protocol):
    def update(self, subject: 'Subject') -> None: ...

class Subject(ABC):
    def __init__(self):
        self._observers: list[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self) -> None:
        for observer in self._observers:
            observer.update(self)

class WeatherStation(Subject):
    def __init__(self):
        super().__init__()
        self._temperature = 0
    
    @property
    def temperature(self) -> float:
        return self._temperature
    
    @temperature.setter
    def temperature(self, value: float) -> None:
        self._temperature = value
        self.notify()
```

## Exercises

1. Create a shape hierarchy using abstract base classes
2. Implement a plugin system using protocols
3. Design a data processing pipeline using the template method pattern
4. Create an event system using the observer pattern
5. Implement a GUI framework using abstract factories