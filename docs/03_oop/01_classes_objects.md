# Python Classes and Objects

## Class Basics

### Class Definition
```python
class Person:
    """A simple class representing a person."""
    
    # Class attribute (shared by all instances)
    species = "Homo sapiens"
    
    # Initialize instance
    def __init__(self, name, age):
        # Instance attributes (unique to each instance)
        self.name = name
        self.age = age
    
    # Instance method
    def greet(self):
        return f"Hello, my name is {self.name}"
```

### Creating Objects
```python
# Create instances
person1 = Person("Alice", 30)
person2 = Person("Bob", 25)

# Access attributes
print(person1.name)         # Alice
print(person2.age)          # 25
print(person1.species)      # Homo sapiens

# Call methods
print(person1.greet())      # Hello, my name is Alice
```

## Class Components

### Class Attributes
```python
class Circle:
    # Class attributes
    pi = 3.14159
    circle_count = 0
    
    def __init__(self, radius):
        self.radius = radius
        Circle.circle_count += 1
    
    @classmethod
    def from_diameter(cls, diameter):
        return cls(diameter / 2)
    
    def area(self):
        return Circle.pi * self.radius ** 2

# Using class attributes
circle = Circle(5)
print(Circle.circle_count)  # 1
print(circle.pi)           # 3.14159
```

### Instance Attributes
```python
class BankAccount:
    def __init__(self, account_number, balance=0):
        # Instance attributes
        self.account_number = account_number
        self.balance = balance
        self._transactions = []  # Protected attribute
        
    def deposit(self, amount):
        self.balance += amount
        self._transactions.append(f"Deposit: {amount}")
    
    def get_balance(self):
        return self.balance
```

### Methods

#### Instance Methods
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # Regular instance method
    def area(self):
        return self.width * self.height
    
    # Method with parameters
    def resize(self, width, height):
        self.width = width
        self.height = height
```

#### Class Methods
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

# Using class methods
date = Date.from_string('2025-04-28')
today = Date.today()
```

#### Static Methods
```python
class MathOperations:
    @staticmethod
    def add(x, y):
        return x + y
    
    @staticmethod
    def is_positive(x):
        return x > 0

# Using static methods
print(MathOperations.add(5, 3))      # 8
print(MathOperations.is_positive(5))  # True
```

## Special Methods

### String Representation
```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
    
    # Informal string representation
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    # Formal string representation
    def __repr__(self):
        return f"Book(title='{self.title}', author='{self.author}')"

book = Book("1984", "George Orwell")
print(str(book))   # 1984 by George Orwell
print(repr(book))  # Book(title='1984', author='George Orwell')
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
    
    # Python automatically provides __gt__, __ge__ based on __lt__

t1 = Temperature(20)
t2 = Temperature(25)
print(t1 < t2)    # True
print(t1 == t2)   # False
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
    
    def __setitem__(self, position, card):
        self.cards[position] = card
    
    def __delitem__(self, position):
        del self.cards[position]
    
    def __contains__(self, card):
        return card in self.cards

deck = Deck()
deck.cards = ["A♠", "K♠", "Q♠"]
print(len(deck))        # 3
print(deck[0])         # A♠
print("K♠" in deck)    # True
```

## Properties and Encapsulation

### Properties
```python
class Employee:
    def __init__(self, first_name, last_name, salary):
        self._first_name = first_name
        self._last_name = last_name
        self._salary = salary
    
    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"
    
    @property
    def salary(self):
        return self._salary
    
    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value
    
    @salary.deleter
    def salary(self):
        self._salary = 0

emp = Employee("John", "Doe", 50000)
print(emp.full_name)  # John Doe
emp.salary = 60000    # Using setter
del emp.salary        # Using deleter
```

### Private Attributes
```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance    # Private attribute
        self._log = []             # Protected attribute
    
    def deposit(self, amount):
        self.__balance += amount
        self._log.append(f"Deposit: {amount}")
    
    def get_balance(self):
        return self.__balance

account = BankAccount(1000)
# print(account.__balance)  # AttributeError
print(account.get_balance())  # 1000
```

## Best Practices

### Clean Class Design
```python
class User:
    """
    A class representing a user in the system.
    
    Attributes:
        username (str): The user's username
        email (str): The user's email address
        is_active (bool): Whether the user account is active
    """
    
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = True
    
    def deactivate(self):
        """Deactivate the user account."""
        self.is_active = False
    
    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"User {self.username} ({status})"
```

### Single Responsibility Principle
```python
# Bad: Class does too many things
class UserManager:
    def create_user(self): pass
    def send_email(self): pass
    def generate_report(self): pass

# Good: Split into focused classes
class UserManager:
    def create_user(self): pass
    def delete_user(self): pass

class EmailService:
    def send_email(self): pass

class ReportGenerator:
    def generate_report(self): pass
```

## Common Patterns

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
        raise ValueError(f"Invalid animal type: {animal_type}")
```

### Singleton Pattern
```python
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Initialize only once
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.data = []
```

## Practice Examples

```python
# 1. Shape hierarchy
class Shape:
    def area(self):
        raise NotImplementedError
    
    def perimeter(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

# 2. Simple data validator
class DataValidator:
    @staticmethod
    def validate_email(email):
        import re
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def validate_phone(phone):
        import re
        pattern = r'^\d{10}$'
        return bool(re.match(pattern, phone))
```

## Exercises

1. Create a Bank Account class with deposit, withdraw, and transfer methods
2. Implement a simple Employee hierarchy with different types of employees
3. Create a Temperature class that can convert between Celsius and Fahrenheit
4. Design a Library catalog system using classes
5. Implement a logging system using the Singleton pattern