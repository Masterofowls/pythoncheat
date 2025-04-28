# Python Dictionaries

## Dictionary Basics

### Creating Dictionaries
```python
# Empty dictionary
empty_dict = {}
empty_dict = dict()

# Dictionary with initial key-value pairs
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Dict from sequences
keys = ["a", "b", "c"]
values = [1, 2, 3]
mapping = dict(zip(keys, values))  # {'a': 1, 'b': 2, 'c': 3}

# Dict comprehension
squares = {x: x**2 for x in range(5)}  # {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Accessing Elements
```python
person = {"name": "Alice", "age": 30, "city": "New York"}

# Using square bracket notation
name = person["name"]  # "Alice"

# Using get() method (safe access)
age = person.get("age")  # 30
country = person.get("country", "Unknown")  # "Unknown" (default value)

# Accessing all values
keys = person.keys()      # dict_keys(['name', 'age', 'city'])
values = person.values()  # dict_values(['Alice', 30, 'New York'])
items = person.items()    # dict_items([('name', 'Alice'), ('age', 30), ('city', 'New York')])
```

## Dictionary Operations

### Modifying Dictionaries
```python
person = {"name": "Alice"}

# Adding/updating items
person["age"] = 30
person.update({"city": "New York", "email": "alice@email.com"})

# Removing items
removed_age = person.pop("age")  # Removes and returns value
removed_item = person.popitem()  # Removes and returns last item
del person["city"]              # Removes key-value pair
person.clear()                  # Removes all items
```

### Dictionary Methods
```python
# Create example dictionary
data = {"a": 1, "b": 2}

# Copy dictionary
shallow_copy = data.copy()
deep_copy = copy.deepcopy(data)

# Set default value
value = data.setdefault("c", 0)  # Adds key if not present

# fromkeys() - Create dict with default values
keys = ["x", "y", "z"]
new_dict = dict.fromkeys(keys, 0)  # {'x': 0, 'y': 0, 'z': 0}
```

## Advanced Dictionary Operations

### Dictionary Merging
```python
# Python 3.5+
dict1 = {"a": 1, "b": 2}
dict2 = {"b": 3, "c": 4}

# Merge with update
merged1 = dict1.copy()
merged1.update(dict2)  # {'a': 1, 'b': 3, 'c': 4}

# Merge with | operator (Python 3.9+)
merged2 = dict1 | dict2  # {'a': 1, 'b': 3, 'c': 4}
```

### Dictionary Views
```python
data = {"a": 1, "b": 2, "c": 3}

# Views are dynamic
keys = data.keys()
values = data.values()
items = data.items()

data["d"] = 4  # Views update automatically
print(keys)    # dict_keys(['a', 'b', 'c', 'd'])
```

### Dictionary Comprehension
```python
# Simple dict comprehension
squares = {x: x**2 for x in range(5)}

# Conditional dict comprehension
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}

# Dict comprehension with multiple conditions
complex_dict = {
    k: v for k, v in zip(range(5), "abcde")
    if k % 2 == 0 and v not in "aeiou"
}
```

## Nested Dictionaries

### Creating and Accessing Nested Dictionaries
```python
# Nested dictionary
users = {
    "alice": {
        "name": "Alice Smith",
        "age": 30,
        "address": {
            "street": "123 Main St",
            "city": "New York"
        }
    },
    "bob": {
        "name": "Bob Johnson",
        "age": 25,
        "address": {
            "street": "456 Oak Ave",
            "city": "Boston"
        }
    }
}

# Accessing nested values
alice_city = users["alice"]["address"]["city"]
bob_info = users.get("bob", {}).get("age")  # Safe nested access
```

### Modifying Nested Dictionaries
```python
# Update nested value
users["alice"]["address"]["zip"] = "10001"

# Deep update
def deep_update(d, key, value):
    keys = key.split('.')
    current = d
    for k in keys[:-1]:
        current = current.setdefault(k, {})
    current[keys[-1]] = value

# Usage
deep_update(users, "alice.address.country", "USA")
```

## Best Practices

### Key Selection
```python
# Good key choices
config = {
    "app_name": "MyApp",
    "version": "1.0.0",
    (2023, 1): "January Report"  # Tuple as immutable key
}

# Bad key choices (mutable objects)
bad_dict = {
    [1, 2]: "value",     # TypeError: unhashable type: 'list'
    {"a": 1}: "value"    # TypeError: unhashable type: 'dict'
}
```

### Dictionary vs Other Data Structures
```python
# Dictionary for lookups (O(1) complexity)
phone_book = {"Alice": "123-456", "Bob": "789-012"}
alice_number = phone_book["Alice"]

# List for ordered data (O(n) lookup)
contacts = [("Alice", "123-456"), ("Bob", "789-012")]
alice_number = next(num for name, num in contacts if name == "Alice")
```

### Memory Management
```python
# Use generator for large data processing
def process_items(items):
    return ((k, v * 2) for k, v in items.items())

# Instead of
# def process_items(items):
#     return {k: v * 2 for k, v in items.items()}
```

## Common Patterns

### Default Dictionaries
```python
from collections import defaultdict

# Count occurrences
words = ["apple", "banana", "apple", "cherry"]
counts = defaultdict(int)
for word in words:
    counts[word] += 1

# Grouping
data = [("A", 1), ("B", 2), ("A", 3)]
groups = defaultdict(list)
for key, value in data:
    groups[key].append(value)
```

### OrderedDict (Pre-Python 3.7)
```python
from collections import OrderedDict

# Maintain insertion order
ordered = OrderedDict()
ordered["first"] = 1
ordered["second"] = 2
ordered["third"] = 3

# Compare with order sensitivity
od1 = OrderedDict({"a": 1, "b": 2})
od2 = OrderedDict({"b": 2, "a": 1})
print(od1 == od2)  # False
```

## Common Pitfalls

### Mutable Default Values
```python
# Bad
def add_user(name, info={}):  # Mutable default value
    info["name"] = name
    return info

# Good
def add_user(name, info=None):
    if info is None:
        info = {}
    info["name"] = name
    return info
```

### Key Errors
```python
data = {"a": 1}

# Bad
try:
    value = data["b"]
except KeyError:
    value = 0

# Good
value = data.get("b", 0)
```

### Dictionary Aliasing
```python
# Shallow copy issue
original = {"numbers": [1, 2, 3]}
copy = original.copy()
copy["numbers"].append(4)  # Modifies both dictionaries!

# Solution: Deep copy
import copy
deep_copy = copy.deepcopy(original)
```

## Practice Examples

```python
# 1. Merge and transform dictionaries
def merge_and_transform(dict1, dict2, transform_fn):
    return {
        k: transform_fn(v)
        for k, v in {**dict1, **dict2}.items()
    }

# Usage
result = merge_and_transform(
    {"a": 1, "b": 2},
    {"b": 3, "c": 4},
    lambda x: x * 2
)

# 2. Nested dictionary access
def safe_get(dictionary, path, default=None):
    keys = path.split('.')
    try:
        return reduce(lambda d, key: d[key], keys, dictionary)
    except (KeyError, TypeError):
        return default

# 3. Dictionary inverse
def inverse_dict(d):
    return {v: k for k, v in d.items()}
```

## Exercises

1. Implement a function that flattens a nested dictionary
2. Create a frequency counter for characters in a string using defaultdict
3. Write a function to find the difference between two dictionaries
4. Implement a cache decorator using a dictionary
5. Create a simple JSON-like data validator using nested dictionaries