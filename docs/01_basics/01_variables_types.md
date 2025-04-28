# Python Variables and Data Types

## Variables

Variables in Python are dynamically typed and case-sensitive. They can be assigned using the `=` operator.

```python
name = "John"      # String
age = 25          # Integer
height = 1.75     # Float
is_student = True # Boolean
```

## Basic Data Types

### Numbers
```python
# Integers
x = 5
big_number = 1_000_000  # Underscores for readability

# Floating-point numbers
pi = 3.14159
scientific = 1.23e-4

# Complex numbers
complex_num = 3 + 4j
```

### Strings
```python
# String creation
single_quotes = 'Hello'
double_quotes = "World"
multiline = '''This is a
multiline string'''

# String operations
name = "Python"
print(name[0])      # 'P'
print(name[-1])     # 'n'
print(name[1:4])    # 'yth'
print(name * 2)     # 'PythonPython'
print(len(name))    # 6
```

### Booleans
```python
# Boolean values
is_true = True
is_false = False

# Boolean operations
print(True and False)  # False
print(True or False)   # True
print(not True)        # False
```

### None Type
```python
# None represents absence of value
empty = None
print(empty is None)  # True
```

## Type Conversion

```python
# Converting between types
str_num = "123"
num = int(str_num)    # String to integer
float_num = float(num)  # Integer to float
str_back = str(num)   # Number to string
```

## Type Checking

```python
x = 42
print(type(x))        # <class 'int'>
isinstance(x, int)    # True
isinstance(x, (int, float))  # True (checks multiple types)
```

## Memory Management

Variables in Python:
- Are references to objects
- Don't need explicit declaration
- Are garbage collected automatically
- Can be deleted using `del`

```python
x = 42
y = x    # y references the same object as x
del x    # Removes reference to object
```

## Best Practices

1. Use descriptive variable names
2. Follow PEP 8 naming conventions:
   - `lowercase_with_underscores` for variables
   - `UPPERCASE_WITH_UNDERSCORES` for constants
3. Avoid using reserved keywords
4. Initialize variables before using them
5. Use type hints for better code clarity (Python 3.5+)

```python
# Type hints example
from typing import List, Dict, Optional

def process_data(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

name: str = "Python"
age: Optional[int] = None
```

## Common Pitfalls

1. Mutable Default Arguments
```python
# Bad
def add_item(item, items=[]):  # Default list is shared
    items.append(item)
    return items

# Good
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

2. Integer Cache
```python
# Small integers (-5 to 256) are cached
a = 256
b = 256
print(a is b)  # True

c = 257
d = 257
print(c is d)  # False (use == for value comparison)
```

## Practice Examples

```python
# 1. Basic variable usage
name = "Alice"
age = 30
height = 1.65
print(f"{name} is {age} years old and {height}m tall")

# 2. Type conversion
price_str = "19.99"
quantity = 3
total = float(price_str) * quantity
print(f"Total: ${total:.2f}")

# 3. Working with multiple types
mixed_list = [1, "hello", 3.14, True]
for item in mixed_list:
    print(f"Value: {item}, Type: {type(item)}")
```

## Exercises

1. Create variables of each basic type and print their types
2. Convert a string of comma-separated numbers into a list of integers
3. Create a dictionary mixing different data types as values
4. Use type hints to declare a function that processes multiple data types