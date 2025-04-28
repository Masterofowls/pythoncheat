# Python Abstractions

## Abstract Base Classes (ABC)

### Basic ABC Usage
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """Abstract base class for shapes"""
    
    @abstractmethod
    def area(self):
        """Calculate area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate perimeter of the shape"""
        pass
    
    @abstractmethod
    def draw(self):
        """Draw the shape"""
        pass

# Cannot instantiate abstract class
# shape = Shape()  # TypeError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius
    
    def draw(self):
        return f"Drawing circle with radius {self.radius}"
```

### Abstract Properties
```python
from abc import ABC, abstractmethod

class Vehicle(ABC):
    @property
    @abstractmethod
    def wheel_count(self):
        """Number of wheels"""
        pass
    
    @property
    @abstractmethod
    def fuel_type(self):
        """Type of fuel used"""
        pass
    
    @abstractmethod
    def start_engine(self):
        """Start the vehicle's engine"""
        pass

class Car(Vehicle):
    @property
    def wheel_count(self):
        return 4
    
    @property
    def fuel_type(self):
        return "gasoline"
    
    def start_engine(self):
        return "Car engine starting..."
```

## Interfaces

### Informal Interfaces
```python
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Movable(ABC):
    @abstractmethod
    def move(self, x, y):
        pass

class Resizable(ABC):
    @abstractmethod
    def resize(self, factor):
        pass

class GameSprite(Drawable, Movable, Resizable):
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
    
    def draw(self):
        return f"Drawing sprite at ({self.x}, {self.y})"
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def resize(self, factor):
        self.size *= factor
```

### Protocol Classes (Python 3.8+)
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Printable(Protocol):
    def print(self) -> str:
        ...

@runtime_checkable
class Serializable(Protocol):
    def to_dict(self) -> dict:
        ...
    
    def from_dict(self, data: dict) -> None:
        ...

class Document:
    def __init__(self, content: str):
        self.content = content
    
    def print(self) -> str:
        return f"Printing: {self.content}"
    
    def to_dict(self) -> dict:
        return {"content": self.content}
    
    def from_dict(self, data: dict) -> None:
        self.content = data["content"]

# Runtime protocol checking
doc = Document("Hello")
print(isinstance(doc, Printable))      # True
print(isinstance(doc, Serializable))   # True
```

## Abstract Methods and Properties

### Abstract Method Patterns
```python
from abc import ABC, abstractmethod
from typing import List, Optional

class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: List[str]) -> List[str]:
        """Process the input data"""
        pass
    
    @abstractmethod
    def validate(self, data: List[str]) -> bool:
        """Validate the input data"""
        pass
    
    def run(self, data: List[str]) -> Optional[List[str]]:
        """Template method that runs the processing pipeline"""
        if self.validate(data):
            return self.process(data)
        return None

class UpperCaseProcessor(DataProcessor):
    def process(self, data: List[str]) -> List[str]:
        return [item.upper() for item in data]
    
    def validate(self, data: List[str]) -> bool:
        return all(isinstance(item, str) for item in data)
```

### Abstract Property Patterns
```python
class Shape(ABC):
    @property
    @abstractmethod
    def vertices(self) -> List[tuple]:
        """Get the vertices of the shape"""
        pass
    
    @property
    @abstractmethod
    def center(self) -> tuple:
        """Get the center point of the shape"""
        pass
    
    @property
    def bounding_box(self) -> tuple:
        """Calculate bounding box from vertices"""
        if not self.vertices:
            return (0, 0, 0, 0)
        x_coords = [v[0] for v in self.vertices]
        y_coords = [v[1] for v in self.vertices]
        return (min(x_coords), min(y_coords), 
                max(x_coords), max(y_coords))

class Rectangle(Shape):
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
    
    @property
    def vertices(self) -> List[tuple]:
        return [(self._x, self._y),
                (self._x + self._width, self._y),
                (self._x + self._width, self._y + self._height),
                (self._x, self._y + self._height)]
    
    @property
    def center(self) -> tuple:
        return (self._x + self._width/2, 
                self._y + self._height/2)
```

## Advanced Abstraction Patterns

### Composable Abstractions
```python
class Renderer(ABC):
    @abstractmethod
    def render(self, data: str) -> str:
        pass

class HTMLRenderer(Renderer):
    def render(self, data: str) -> str:
        return f"<p>{data}</p>"

class MarkdownRenderer(Renderer):
    def render(self, data: str) -> str:
        return f"**{data}**"

class Document:
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
        self.content = []
    
    def add_content(self, content: str):
        self.content.append(content)
    
    def render(self) -> str:
        return "\n".join(
            self.renderer.render(item) 
            for item in self.content
        )
```

### Abstract Factory Pattern
```python
class UIElement(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Button(UIElement):
    @abstractmethod
    def click(self) -> str:
        pass

class TextBox(UIElement):
    @abstractmethod
    def get_text(self) -> str:
        pass

class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_textbox(self) -> TextBox:
        pass

class ModernButton(Button):
    def render(self) -> str:
        return "Rendering modern button"
    
    def click(self) -> str:
        return "Clicked modern button"

class ModernTextBox(TextBox):
    def render(self) -> str:
        return "Rendering modern textbox"
    
    def get_text(self) -> str:
        return "Modern textbox content"

class ModernUIFactory(UIFactory):
    def create_button(self) -> Button:
        return ModernButton()
    
    def create_textbox(self) -> TextBox:
        return ModernTextBox()
```

## Best Practices

### Design by Contract
```python
from abc import ABC, abstractmethod
from typing import List, Any

class DataValidator(ABC):
    @abstractmethod
    def validate(self, data: Any) -> bool:
        """
        Validate input data
        
        Precondition: data must not be None
        Postcondition: returns True if data is valid
        """
        pass

class DataTransformer(ABC):
    @abstractmethod
    def transform(self, data: Any) -> Any:
        """
        Transform input data
        
        Precondition: data must be valid
        Postcondition: returned data must be transformed
        """
        pass

class Pipeline:
    def __init__(self, validator: DataValidator, 
                 transformer: DataTransformer):
        self.validator = validator
        self.transformer = transformer
    
    def process(self, data: Any) -> Any:
        """
        Process data through the pipeline
        
        Preconditions:
        - data must not be None
        - validator must be set
        - transformer must be set
        
        Postconditions:
        - returns None if data is invalid
        - returns transformed data if valid
        """
        assert data is not None, "Data cannot be None"
        if self.validator.validate(data):
            return self.transformer.transform(data)
        return None
```

### Dependency Inversion
```python
class MessageSender(ABC):
    @abstractmethod
    def send(self, message: str) -> bool:
        pass

class EmailSender(MessageSender):
    def send(self, message: str) -> bool:
        # Email sending logic
        return True

class SMSSender(MessageSender):
    def send(self, message: str) -> bool:
        # SMS sending logic
        return True

class NotificationService:
    def __init__(self, sender: MessageSender):
        self.sender = sender
    
    def notify(self, message: str) -> bool:
        return self.sender.send(message)
```

## Exercises

1. Create an abstract shape hierarchy with different shape implementations
2. Implement a plugin system using abstract base classes
3. Design a composite pattern using abstractions
4. Build a data processing pipeline using abstract classes
5. Create a strategy pattern implementation using protocols