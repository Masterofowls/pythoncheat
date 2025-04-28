# Python Classes and Objects

## Class Basics

### Class Definition
```python
class Person:
    """A simple class representing a person."""
    
    # Class variable (shared by all instances)
    species = "Homo sapiens"
    
    # Constructor (initialization)
    def __init__(self, name, age):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age
    
    # Instance method
    def greet(self):
        return f"Hello, I'm {self.name}"
    
    # String representation
    def __str__(self):
        return f"{self.name} ({self.age} years old)"
```

### Creating Objects
```python
# Creating instances
person1 = Person("Alice", 25)
person2 = Person("Bob", 30)

# Accessing attributes and methods
print(person1.name)         # Alice
print(person1.greet())      # Hello, I'm Alice
print(person1)              # Alice (25 years old)

# Accessing class variables
print(Person.species)       # Homo sapiens
print(person1.species)      # Homo sapiens
```

## Class and Instance Variables

### Class Variables
```python
class Employee:
    # Class variables
    company = "Tech Corp"
    employee_count = 0
    
    def __init__(self, name):
        self.name = name
        Employee.employee_count += 1
    
    @classmethod
    def get_company_info(cls):
        return f"{cls.company} has {cls.employee_count} employees"
```

### Instance Variables
```python
class BankAccount:
    # Class variable
    interest_rate = 0.02
    
    def __init__(self, account_number, balance):
        # Instance variables
        self.account_number = account_number
        self.balance = balance
        self._transactions = []  # Protected instance variable
    
    def deposit(self, amount):
        self.balance += amount
        self._transactions.append(("deposit", amount))
```

## Methods

### Instance Methods
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
```

### Class Methods
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
        today = datetime.datetime.now()
        return cls(today.year, today.month, today.day)
```

### Static Methods
```python
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y
    
    @staticmethod
    def is_positive(x):
        return x > 0
```

## Special Methods

### Constructor and Destructor
```python
class Resource:
    def __init__(self, name):
        self.name = name
        print(f"Resource {name} initialized")
    
    def __del__(self):
        print(f"Resource {self.name} cleaned up")
```

### String Representation
```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"Point({self.x}, {self.y})"
    
    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
```

### Comparison Methods
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius
    
    def __eq__(self, other):
        return self.celsius == other.celsius
    
    def __lt__(self, other):
        return self.celsius < other.celsius
    
    def __le__(self, other):
        return self.celsius <= other.celsius
```

### Container Methods
```python
class Deck:
    def __init__(self):
        self.cards = []
    
    def __len__(self):
        return len(self.cards)
    
    def __getitem__(self, position):
        return self.cards[position]
    
    def __setitem__(self, position, value):
        self.cards[position] = value
    
    def __contains__(self, card):
        return card in self.cards
```

## Properties

### Basic Properties
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

### Property Decorators
```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self._celsius = (value - 32) * 5/9
```

## Best Practices

### Encapsulation
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance  # Protected
        self.__account_number = None  # Private
    
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self._log_transaction("deposit", amount)
    
    def _log_transaction(self, type_, amount):
        # Protected method
        pass
```

### Data Validation
```python
class Person:
    def __init__(self, name, age):
        self.name = name  # This will call the setter
        self.age = age    # This will call the setter
    
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be an integer")
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
```

## Common Patterns

### Singleton Pattern
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Pattern
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type == "dog":
            return Dog()
        elif animal_type == "cat":
            return Cat()
        raise ValueError("Unknown animal type")
```

### Context Manager
```python
class File:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.file.close()
```

## Exercises

1. Create a class hierarchy for different shapes (Circle, Rectangle, Triangle)
2. Implement a custom container class that behaves like a list
3. Create a class that implements the context manager protocol
4. Build a simple class-based cache system with size limit
5. Design a class for handling temperature conversions between units