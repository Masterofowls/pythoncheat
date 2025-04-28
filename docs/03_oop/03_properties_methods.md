# Python Properties and Methods

## Properties

### Basic Property Usage
```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return (self._celsius * 9/5) + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

# Using properties
temp = Temperature()
temp.celsius = 25              # Using celsius setter
print(temp.fahrenheit)         # Using fahrenheit getter
temp.fahrenheit = 100         # Using fahrenheit setter
print(temp.celsius)           # Using celsius getter
```

### Property Decorators

#### Read-Only Properties
```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2
    
    @property
    def circumference(self):
        return 2 * 3.14159 * self._radius

circle = Circle(5)
print(circle.area)           # Can read
# circle.area = 50          # AttributeError: can't set attribute
```

#### Property with Validation
```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
    
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
        if not isinstance(value, (int, float)):
            raise TypeError("Age must be a number")
        if value < 0:
            raise ValueError("Age cannot be negative")
        self._age = value
```

### Computed Properties
```python
from datetime import datetime

class Employee:
    def __init__(self, first_name, last_name, birth_year):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_year = birth_year
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        return datetime.now().year - self.birth_year
    
    @property
    def email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@company.com"
```

## Methods

### Instance Methods
```python
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance
        self._transactions = []
    
    def deposit(self, amount):
        """Instance method that modifies object state"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        self._transactions.append(("deposit", amount))
        return self._balance
    
    def get_transaction_history(self):
        """Instance method that accesses object state"""
        return self._transactions.copy()
    
    def transfer(self, other_account, amount):
        """Instance method that interacts with other objects"""
        self._balance -= amount
        other_account.deposit(amount)
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
        """Create instance from string YYYY-MM-DD"""
        year, month, day = map(int, date_string.split('-'))
        return cls(year, month, day)
    
    @classmethod
    def today(cls):
        """Create instance with today's date"""
        from datetime import datetime
        today = datetime.now()
        return cls(today.year, today.month, today.day)
    
    @classmethod
    def validate(cls, year, month, day):
        """Validate date parameters"""
        if not (1 <= month <= 12):
            raise ValueError("Invalid month")
        if not (1 <= day <= 31):
            raise ValueError("Invalid day")
        return True
```

### Static Methods
```python
class MathOperations:
    @staticmethod
    def is_even(num):
        return num % 2 == 0
    
    @staticmethod
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num ** 0.5) + 1):
            if num % i == 0:
                return False
        return True
    
    @staticmethod
    def factorial(num):
        if num < 0:
            raise ValueError("Factorial not defined for negative numbers")
        if num == 0:
            return 1
        return num * MathOperations.factorial(num - 1)
```

## Advanced Method Patterns

### Method Chaining
```python
class QueryBuilder:
    def __init__(self):
        self.query = []
        self.params = []
    
    def select(self, *fields):
        self.query.append(f"SELECT {', '.join(fields)}")
        return self
    
    def from_table(self, table):
        self.query.append(f"FROM {table}")
        return self
    
    def where(self, condition, param):
        self.query.append(f"WHERE {condition}")
        self.params.append(param)
        return self
    
    def build(self):
        return " ".join(self.query), tuple(self.params)

# Using method chaining
query = (QueryBuilder()
         .select("name", "age")
         .from_table("users")
         .where("age > ?", 18)
         .build())
```

### Context Manager Methods
```python
class DatabaseConnection:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        """Set up the context"""
        self.connection = self.connect()
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the context"""
        if self.connection:
            self.connection.close()
    
    def connect(self):
        # Simulated database connection
        print(f"Connecting to {self.connection_string}")
        return self

# Using as context manager
with DatabaseConnection("mysql://localhost") as conn:
    # Work with database
    pass  # Connection automatically closed
```

### Descriptor Methods
```python
class Validator:
    def __init__(self, min_value=None, max_value=None):
        self.min_value = min_value
        self.max_value = max_value
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__.get(self.name)
    
    def __set__(self, instance, value):
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f"Value must be ≥ {self.min_value}")
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f"Value must be ≤ {self.max_value}")
        instance.__dict__[self.name] = value
    
    def __set_name__(self, owner, name):
        self.name = name

class Product:
    price = Validator(min_value=0)
    quantity = Validator(min_value=0, max_value=100)
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
```

## Best Practices

### Property vs Direct Attribute Access
```python
# Bad: Direct attribute access
class Circle:
    def __init__(self, radius):
        self.radius = radius  # No validation

# Good: Property with validation
class Circle:
    def __init__(self, radius):
        self._radius = 0  # Initialize first
        self.radius = radius  # Use property setter
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value
```

### Method Organization
```python
class DataProcessor:
    """Example of well-organized methods"""
    
    def __init__(self, data):
        self.data = data
    
    # Public interface
    def process(self):
        """Main public method"""
        cleaned_data = self._clean_data()
        normalized_data = self._normalize(cleaned_data)
        return self._format_output(normalized_data)
    
    # Helper methods (private)
    def _clean_data(self):
        """Remove invalid entries"""
        return [x for x in self.data if self._is_valid(x)]
    
    def _normalize(self, data):
        """Normalize the values"""
        return [self._normalize_value(x) for x in data]
    
    def _format_output(self, data):
        """Format the final output"""
        return {
            "processed_data": data,
            "count": len(data)
        }
    
    def _is_valid(self, value):
        """Validate a single value"""
        return value is not None
    
    def _normalize_value(self, value):
        """Normalize a single value"""
        return value / max(self.data)
```

## Common Patterns

### Lazy Properties
```python
class ExpensiveComputation:
    def __init__(self, data):
        self.data = data
        self._cached_result = None
    
    @property
    def result(self):
        if self._cached_result is None:
            # Expensive computation
            print("Computing...")
            self._cached_result = sum(x * x for x in self.data)
        return self._cached_result

comp = ExpensiveComputation(range(1000))
print(comp.result)  # Computes first time
print(comp.result)  # Returns cached value
```

### Factory Methods
```python
class Document:
    def __init__(self, content):
        self.content = content
    
    @classmethod
    def from_file(cls, filename):
        with open(filename, 'r') as f:
            content = f.read()
        return cls(content)
    
    @classmethod
    def from_string(cls, string):
        return cls(string)
    
    @classmethod
    def from_json(cls, json_string):
        import json
        data = json.loads(json_string)
        return cls(data.get('content', ''))
```

## Exercises

1. Create a Temperature class with Celsius and Fahrenheit properties
2. Implement a BankAccount class with properties for balance and methods for transactions
3. Design a Rectangle class with properties for area and perimeter
4. Create a Person class with full_name property and age validation
5. Implement a DataProcessor class with method chaining for data transformations