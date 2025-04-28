# Python Sets

## Set Basics

### Creating Sets
```python
# Empty set
empty_set = set()  # Note: {} creates empty dict, not set

# Set from sequence
numbers = {1, 2, 3, 4, 5}
chars = set("hello")  # {'h', 'e', 'l', 'o'}

# Set comprehension
evens = {x for x in range(10) if x % 2 == 0}  # {0, 2, 4, 6, 8}

# Set from list with duplicates
items = set([1, 2, 2, 3, 3, 4])  # {1, 2, 3, 4}
```

### Set Properties
- Unordered: items have no defined order
- Unique: no duplicates allowed
- Immutable elements: items must be immutable
- Mutable set: can add/remove items

```python
# Valid set elements
valid_set = {1, 3.14, "hello", (1, 2), frozenset([1, 2])}

# Invalid set elements
invalid_set = {[1, 2]}  # TypeError: unhashable type: 'list'
invalid_set = {{1, 2}}  # TypeError: unhashable type: 'set'
```

## Set Operations

### Adding and Removing Elements
```python
numbers = {1, 2, 3}

# Adding elements
numbers.add(4)           # {1, 2, 3, 4}
numbers.update([5, 6])   # {1, 2, 3, 4, 5, 6}

# Removing elements
numbers.remove(6)        # Raises KeyError if not found
numbers.discard(6)       # No error if not found
popped = numbers.pop()   # Remove and return arbitrary element
numbers.clear()          # Remove all elements
```

### Set Mathematical Operations
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union (OR)
union = a | b           # {1, 2, 3, 4, 5, 6}
union = a.union(b)      # Same as above

# Intersection (AND)
common = a & b          # {3, 4}
common = a.intersection(b)  # Same as above

# Difference (items in a but not in b)
diff = a - b            # {1, 2}
diff = a.difference(b)  # Same as above

# Symmetric difference (items in either set but not both)
sym_diff = a ^ b        # {1, 2, 5, 6}
sym_diff = a.symmetric_difference(b)  # Same as above
```

### Set Comparisons
```python
a = {1, 2, 3}
b = {1, 2, 3, 4}
c = {1, 2}

# Subset and superset
print(c.issubset(a))      # True (c ⊆ a)
print(c <= a)             # True (same as above)
print(b.issuperset(a))    # True (b ⊇ a)
print(b >= a)             # True (same as above)

# Proper subset/superset
print(c < a)              # True (c ⊂ a)
print(b > a)              # True (b ⊃ a)

# Disjoint sets (no common elements)
x = {1, 2, 3}
y = {4, 5, 6}
print(x.isdisjoint(y))    # True
```

## Advanced Set Operations

### Multiple Set Operations
```python
a = {1, 2, 3}
b = {2, 3, 4}
c = {3, 4, 5}

# Multiple unions
all_nums = a | b | c    # {1, 2, 3, 4, 5}

# Multiple intersections
common = a & b & c      # {3}

# Complex operations
result = (a | b) & (b | c)  # {2, 3, 4}
```

### Set Comprehensions
```python
# Basic set comprehension
squares = {x**2 for x in range(10)}

# Conditional set comprehension
evens = {x for x in range(10) if x % 2 == 0}

# Nested set comprehension
matrix = {(x, y) for x in range(2) for y in range(2)}
```

### Frozen Sets
```python
# Creating immutable sets
frozen = frozenset([1, 2, 3])

# Use as dictionary keys
set_dict = {
    frozenset([1, 2]): "first",
    frozenset([3, 4]): "second"
}

# Cannot modify frozen sets
# frozen.add(4)  # AttributeError
```

## Common Use Cases

### Removing Duplicates
```python
# Remove duplicates from list
original = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(original))

# Preserve order (Python 3.7+)
from dict.fromkeys
unique_ordered = list(dict.fromkeys(original))
```

### Membership Testing
```python
valid_users = {"alice", "bob", "charlie"}

def check_user(username):
    return username.lower() in valid_users

# Much faster than list for large datasets
print(check_user("Alice".lower()))  # True
```

### Finding Unique Elements
```python
text = "hello world"
unique_chars = set(text)  # {'h', 'e', 'l', 'o', ' ', 'w', 'r', 'd'}

# Count unique elements
def count_unique(sequence):
    return len(set(sequence))
```

## Best Practices

### Set vs List vs Dictionary
```python
# Use set for:
# 1. Membership testing
allowed = {"admin", "user", "guest"}
role = "admin"
is_allowed = role in allowed  # O(1) complexity

# 2. Removing duplicates
unique_numbers = set([1, 2, 2, 3, 3, 3])

# 3. Mathematical set operations
group1 = {"alice", "bob"}
group2 = {"bob", "charlie"}
all_users = group1 | group2
```

### Memory Efficiency
```python
# Generator for large data processing
def unique_items(iterable):
    seen = set()
    for item in iterable:
        if item not in seen:
            seen.add(item)
            yield item
```

## Common Patterns

### Set Operations for Data Analysis
```python
# Finding common elements
def find_common_elements(*sequences):
    return set.intersection(*map(set, sequences))

# Finding unique elements
def find_unique_elements(*sequences):
    return set.union(*map(set, sequences))

# Finding elements in first but not in others
def find_exclusive_elements(first, *others):
    return set(first) - set.union(*map(set, others))
```

### Set as a Filter
```python
# Filter list based on set
allowed = {"jpg", "png", "gif"}
files = ["doc.jpg", "data.txt", "img.png", "file.exe"]
valid_files = [f for f in files if f.split(".")[-1] in allowed]
```

## Common Pitfalls

### Mutable Elements
```python
# Cannot use mutable objects in sets
valid = {(1, 2), "hello", 42}
invalid = {[1, 2]}  # TypeError

# Solution: Convert to tuple
lists = [[1, 2], [3, 4]]
set_of_tuples = {tuple(lst) for lst in lists}
```

### Set Operations vs Methods
```python
a = {1, 2}
b = {2, 3}

# These are equivalent:
union1 = a | b
union2 = a.union(b)

# But this won't work:
# union3 = a | [2, 3]  # TypeError
union4 = a.union([2, 3])  # Works fine
```

### Order Dependence
```python
# Sets are unordered
numbers = {1, 2, 3}
# Don't rely on order when iterating
for num in numbers:  # Order not guaranteed
    print(num)
```

## Practice Examples

```python
# 1. Set-based data deduplication
def deduplicate_preserve_order(sequence):
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]

# 2. Finding all unique combinations
def unique_pairs(items):
    return {
        (a, b) 
        for i, a in enumerate(items) 
        for b in items[i+1:]
    }

# 3. Set-based validation
def validate_categories(categories, allowed_categories):
    invalid = set(categories) - set(allowed_categories)
    return not invalid, invalid
```

## Exercises

1. Implement a function that finds all possible subsets of a set
2. Create a function that checks if two strings are anagrams using sets
3. Write a function that finds the longest substring without repeating characters using sets
4. Implement a simple spell checker using sets
5. Create a function that finds the intersection of multiple sets efficiently