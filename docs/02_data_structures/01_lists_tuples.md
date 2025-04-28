# Lists and Tuples in Python

## Lists

### List Creation
```python
# Empty list
empty_list = []
empty_list = list()

# List with initial values
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True]

# List from other sequences
chars = list("hello")  # ['h', 'e', 'l', 'l', 'o']
numbers = list(range(5))  # [0, 1, 2, 3, 4]

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
```

### List Operations

#### Accessing Elements
```python
numbers = [1, 2, 3, 4, 5]

# Indexing (0-based)
first = numbers[0]     # 1
last = numbers[-1]     # 5

# Slicing [start:end:step]
subset = numbers[1:4]   # [2, 3, 4]
reversed_list = numbers[::-1]  # [5, 4, 3, 2, 1]
every_second = numbers[::2]    # [1, 3, 5]
```

#### Modifying Lists
```python
numbers = [1, 2, 3]

# Adding elements
numbers.append(4)           # [1, 2, 3, 4]
numbers.insert(1, 1.5)     # [1, 1.5, 2, 3, 4]
numbers.extend([5, 6])     # [1, 1.5, 2, 3, 4, 5, 6]

# Removing elements
numbers.remove(1.5)        # Removes first occurrence of 1.5
popped = numbers.pop()     # Removes and returns last element
popped_index = numbers.pop(1)  # Removes element at index 1
del numbers[0]            # Removes element at index 0
numbers.clear()           # Removes all elements
```

#### List Methods
```python
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]

# Sorting
numbers.sort()              # In-place sort
numbers.sort(reverse=True)  # Sort in descending order
sorted_nums = sorted(numbers)  # Returns new sorted list

# Other operations
numbers.reverse()           # Reverses in-place
count = numbers.count(5)    # Counts occurrences of 5
index = numbers.index(4)    # Find index of first 4
```

### List Comprehensions with Conditions
```python
numbers = range(10)

# Single condition
evens = [x for x in numbers if x % 2 == 0]

# Multiple conditions
filtered = [x for x in numbers if x % 2 == 0 and x > 4]

# If-else in comprehension
results = ["even" if x % 2 == 0 else "odd" for x in numbers]
```

## Tuples

### Tuple Creation
```python
# Empty tuple
empty_tuple = ()
empty_tuple = tuple()

# Tuple with elements
numbers = (1, 2, 3)
single_element = (1,)  # Note the comma
mixed = (1, "hello", 3.14)

# Tuple packing
coordinates = 3, 4  # Creates tuple (3, 4)

# Tuple unpacking
x, y = coordinates  # x = 3, y = 4
```

### Tuple Operations

#### Accessing Elements
```python
point = (1, 2, 3)

# Indexing
x = point[0]      # 1
z = point[-1]     # 3

# Slicing
subset = point[1:]  # (2, 3)
```

#### Tuple Methods
```python
numbers = (1, 2, 2, 3, 4, 2)

# Count occurrences
count = numbers.count(2)  # 3

# Find index
index = numbers.index(3)  # 3
```

### Named Tuples
```python
from collections import namedtuple

# Creating named tuple class
Point = namedtuple('Point', ['x', 'y'])
point = Point(3, 4)

# Accessing elements
print(point.x)     # 3
print(point[0])    # 3
x, y = point       # Unpacking

# Methods
point._replace(x=5)  # Creates new Point(5, 4)
point._asdict()      # Creates OrderedDict
```

## Lists vs Tuples

### Key Differences
1. Mutability
   - Lists are mutable (can be modified)
   - Tuples are immutable (cannot be modified)

2. Syntax
   - Lists use square brackets []
   - Tuples use parentheses ()

3. Methods
   - Lists have more methods for modification
   - Tuples have only count() and index()

4. Performance
   - Tuples are slightly more memory efficient
   - Tuples are slightly faster to create and access

### Use Cases
```python
# Lists: When you need a mutable sequence
shopping_cart = ["apple", "banana"]
shopping_cart.append("orange")

# Tuples: For unchangeable data
coordinates = (33.9425, -118.4081)
rgb_color = (255, 128, 0)

# Named Tuples: For simple data structures
Person = namedtuple('Person', ['name', 'age'])
employee = Person("Alice", 30)
```

## Best Practices

1. Choose the Right Type
```python
# Use tuple for fixed data
DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')

# Use list for changing data
scores = [10, 20, 30]
scores.append(40)
```

2. List Comprehension vs Loop
```python
# List comprehension for simple transformations
squares = [x**2 for x in range(10)]

# Loop for complex operations
results = []
for x in range(10):
    if x % 2 == 0:
        # Complex calculation
        results.append(complex_function(x))
```

3. Memory Efficiency
```python
# Generator expression for large sequences
sum(x**2 for x in range(1000000))

# List comprehension for small sequences
squares = [x**2 for x in range(100)]
```

## Common Pitfalls

### List Reference vs Copy
```python
# Shallow copy problem
original = [1, [2, 3], 4]
copy = original[:]  # Creates shallow copy
copy[1][0] = 5     # Modifies both lists!

# Solution: Use deep copy
from copy import deepcopy
deep_copy = deepcopy(original)
```

### Tuple Single Element
```python
# Wrong: creates int
single = (1)

# Correct: creates tuple
single = (1,)
```

### List Multiplication
```python
# Unexpected behavior with nested lists
grid = [[0] * 3] * 3  # Creates references!

# Correct way
grid = [[0] * 3 for _ in range(3)]
```

## Practice Examples

```python
# 1. Custom sorting with key function
students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
sorted_students = sorted(students, key=lambda x: x[1], reverse=True)

# 2. Filtering and mapping
numbers = [1, 2, 3, 4, 5, 6]
odd_squares = [x**2 for x in numbers if x % 2 != 0]

# 3. Working with coordinates
Point = namedtuple('Point', ['x', 'y'])
points = [Point(x, x**2) for x in range(5)]
distances = [(p, (p.x**2 + p.y**2)**0.5) for p in points]
```

## Exercises

1. Create a function that removes duplicates from a list while maintaining order
2. Implement a function that finds all pairs of numbers in a list that sum to a target
3. Write a function that rotates a list by n positions
4. Create a function that merges two sorted lists into a single sorted list
5. Implement a stack data structure using a list