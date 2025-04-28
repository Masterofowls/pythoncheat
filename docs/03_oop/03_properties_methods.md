# Python Properties and Methods

## Properties

### Basic Property Usage
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        """Get the circle's radius"""
        return self._radius
    
    @radius.setter
    def radius(self, value):
        """Set the circle's radius"""
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def area(self):
        """Calculate area of the circle"""
        return 3.14159 * self._radius ** 2
    
    @property
    def circumference(self):
        """Calculate circumference of the circle"""
        return 2 * 3.14159 * self._radius
```

### Property Decorators
```python
class Temperature:
    def __init__(self):
        self._celsius = 0
    
    # Getter
    @property
    def celsius(self):
        return self._celsius
    
    # Setter
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    # Deleter
    @celsius.deleter
    def celsius(self):
        print("Resetting temperature...")
        self._celsius = 0
    
    # Read-only property
    @property
    def kelvin(self):
        return self._celsius + 273.15
```

### Property Factory Function
```python
class Person:
    def __init__(self):
        self._name = ''
    
    # Using property() function
    def get_name(self):
        return self._name
    
    def set_name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string")
        self._name = value
    
    def del_name(self):
        del self._name
    
    name = property(
        fget=get_name,
        fset=set_name,
        fdel=del_name,
        doc="The person's name"
    )
```

## Methods

### Instance Methods
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    # Regular instance method
    def area(self):
        return self.width * self.height
    
    # Method with parameters
    def resize(self, width_factor, height_factor):
        self.width *= width_factor
        self.height *= height_factor
    
    # Method that returns multiple values
    def dimensions(self):
        return self.width, self.height
```

### Class Methods
```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
    
    @classmethod
    def from_string(cls, date_str):
        """Create a Date object from a string"""
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Create a Date object with today's date"""
        import datetime
        today = datetime.datetime.now()
        return cls(today.year, today.month, today.day)
```

### Static Methods
```python
class MathUtils:
    @staticmethod
    def is_even(number):
        return number % 2 == 0
    
    @staticmethod
    def is_prime(number):
        if number < 2:
            return False
        for i in range(2, int(number ** 0.5) + 1):
            if number % i == 0:
                return False
        return True
    
    @staticmethod
    def factorial(number):
        if number < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        if number == 0:
            return 1
        return number * MathUtils.factorial(number - 1)
```

## Private and Protected Members

### Name Mangling
```python
class Account:
    def __init__(self, balance):
        self.__balance = balance  # Private attribute
        self._transactions = []   # Protected attribute
    
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            self._transactions.append(('deposit', amount))
    
    def __update_balance(self):  # Private method
        # Internal processing
        pass
    
    def _validate_transaction(self):  # Protected method
        # Validation logic
        pass
```

### Property Access Control
```python
class Employee:
    def __init__(self):
        self.__salary = 0
        self.__name = ''
    
    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if self.__validate_salary(value):
            self.__salary = value
    
    def __validate_salary(self, value):
        return isinstance(value, (int, float)) and value >= 0
```

## Method Types and Usage

### Magic Methods
```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

### Method Chaining
```python
class StringBuilder:
    def __init__(self):
        self._strings = []
    
    def append(self, string):
        self._strings.append(string)
        return self
    
    def prepend(self, string):
        self._strings.insert(0, string)
        return self
    
    def remove_last(self):
        if self._strings:
            self._strings.pop()
        return self
    
    def build(self):
        return ''.join(self._strings)
```

## Advanced Property Patterns

### Computed Properties
```python
class Rectangle:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._area = None
        self._perimeter = None
    
    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        # Invalidate cached computations
        self._area = None
        self._perimeter = None
    
    @property
    def area(self):
        if self._area is None:
            self._area = self._width * self._height
        return self._area
```

### Property Dependencies
```python
class Person:
    def __init__(self, first_name, last_name):
        self._first_name = first_name
        self._last_name = last_name
        self._full_name = None
    
    @property
    def first_name(self):
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        self._first_name = value
        self._full_name = None  # Invalidate cached full name
    
    @property
    def full_name(self):
        if self._full_name is None:
            self._full_name = f"{self._first_name} {self._last_name}"
        return self._full_name
```

## Best Practices

### Property Usage Guidelines
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance
    
    # Use properties for computed or validated attributes
    @property
    def balance(self):
        return self._balance
    
    # Use properties to encapsulate business logic
    @property
    def is_overdrawn(self):
        return self._balance < 0
    
    # Use methods for actions
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
```

### Method Naming Conventions
```python
class DataProcessor:
    def process_data(self):
        """Verb phrase for actions"""
        pass
    
    @property
    def is_valid(self):
        """Noun phrase for states/properties"""
        pass
    
    def _internal_helper(self):
        """Underscore prefix for internal methods"""
        pass
    
    def __secure_operation(self):
        """Double underscore for strong privacy"""
        pass
```

## Exercises

1. Create a class with computed properties that cache their values
2. Implement a class with method chaining for building complex objects
3. Design a class with properties that maintain data consistency
4. Create a class using name mangling for secure data handling
5. Implement a class that uses all three types of methods (instance, class, static)