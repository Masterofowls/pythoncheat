# Python Collections Module

## Counter

### Basic Usage
```python
from collections import Counter

# Creating counters
colors = ["red", "blue", "red", "green", "blue", "blue"]
color_count = Counter(colors)  # Counter({'blue': 3, 'red': 2, 'green': 1})

# From string
word_count = Counter("mississippi")  # Counter({'i': 4, 's': 4, 'p': 2, 'm': 1})

# From dictionary
counter = Counter({"a": 2, "b": 3})
```

### Counter Operations
```python
counter = Counter(["a", "b", "b", "c", "c", "c"])

# Most common elements
print(counter.most_common(2))  # [('c', 3), ('b', 2)]

# Updating counter
counter.update(["a", "b", "d"])

# Arithmetic operations
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})
```

## defaultdict

### Basic Usage
```python
from collections import defaultdict

# Create with default factory
int_dict = defaultdict(int)      # Default value: 0
list_dict = defaultdict(list)    # Default value: []
set_dict = defaultdict(set)      # Default value: set()

# Custom default factory
def custom_default():
    return "Not Found"
d = defaultdict(custom_default)
```

### Common Use Cases
```python
# Group items by key
grades = [("Alice", "A"), ("Bob", "B"), ("Alice", "A+")]
student_grades = defaultdict(list)
for student, grade in grades:
    student_grades[student].append(grade)

# Count occurrences
words = ["apple", "banana", "apple", "cherry"]
word_count = defaultdict(int)
for word in words:
    word_count[word] += 1

# Create nested defaultdict
nested = defaultdict(lambda: defaultdict(list))
nested["outer"]["inner"].append("value")
```

## deque (Double-Ended Queue)

### Basic Usage
```python
from collections import deque

# Create deque
d = deque([1, 2, 3])
d = deque(maxlen=3)  # Fixed-length deque

# Basic operations
d.append(4)        # Add to right
d.appendleft(0)    # Add to left
d.pop()            # Remove from right
d.popleft()        # Remove from left
d.extend([4, 5])   # Extend on right
d.extendleft([0])  # Extend on left
```

### Advanced Operations
```python
d = deque([1, 2, 3, 4, 5])

# Rotation
d.rotate(2)    # [4, 5, 1, 2, 3]
d.rotate(-1)   # [5, 1, 2, 3, 4]

# Clear and copy
d.clear()
d_copy = d.copy()

# Count and remove
d = deque([1, 2, 2, 3, 2])
count = d.count(2)    # 3
d.remove(2)          # Removes first occurrence
```

## namedtuple

### Creating Named Tuples
```python
from collections import namedtuple

# Basic creation
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, y=22)

# Alternative field specifications
Person = namedtuple('Person', 'name age city')
Student = namedtuple('Student', 'name, age, grade')
Config = namedtuple('Config', 'host port user pass', defaults=['localhost', 8080])
```

### Operations and Methods
```python
Point = namedtuple('Point', ['x', 'y'])
p = Point(11, 22)

# Accessing values
print(p.x)          # By name
print(p[0])         # By index
x, y = p            # Unpacking

# Converting to dictionary
d = p._asdict()     # OrderedDict([('x', 11), ('y', 22)])

# Creating new instance with changes
p2 = p._replace(x=33)

# Get field names
print(p._fields)    # ('x', 'y')
```

## OrderedDict

### Basic Usage (Pre-Python 3.7)
```python
from collections import OrderedDict

# Create ordered dictionary
d = OrderedDict()
d['first'] = 1
d['second'] = 2
d['third'] = 3

# Create from list of pairs
d = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
```

### Operations
```python
d = OrderedDict()
d['a'] = 1
d['b'] = 2

# Move to end
d.move_to_end('a')          # Move to last
d.move_to_end('b', False)   # Move to first

# Pop items
last = d.popitem()          # Remove last item
first = d.popitem(False)    # Remove first item
```

## ChainMap

### Basic Usage
```python
from collections import ChainMap

# Create ChainMap
defaults = {'color': 'red', 'user': 'guest'}
user_settings = {'color': 'blue'}
cm = ChainMap(user_settings, defaults)

# Accessing values
print(cm['color'])    # 'blue' (from user_settings)
print(cm['user'])     # 'guest' (from defaults)
```

### Operations
```python
# Adding new maps
new_settings = {'color': 'green', 'theme': 'dark'}
cm2 = cm.new_child(new_settings)

# Accessing parents
parent = cm.parents   # Get ChainMap without first map

# Update and delete
cm2['color'] = 'yellow'   # Only updates in first map
del cm2['color']         # Only deletes from first map
```

## UserDict, UserList, and UserString

### UserDict Example
```python
from collections import UserDict

class CustomDict(UserDict):
    def __setitem__(self, key, value):
        super().__setitem__(key.lower(), value)
    
    def __getitem__(self, key):
        return super().__getitem__(key.lower())

d = CustomDict({"Name": "John", "AGE": 30})
print(d["name"])  # "John"
```

### UserList Example
```python
from collections import UserList

class CustomList(UserList):
    def append(self, item):
        if isinstance(item, (int, float)):
            super().append(item)
    
    def extend(self, items):
        for item in items:
            self.append(item)

numbers = CustomList([1, 2, 3])
numbers.append("4")  # Won't be added
numbers.append(4)    # Will be added
```

## Best Practices

### Choosing the Right Collection
```python
# Counter for counting
words = ["apple", "banana", "apple"]
counts = Counter(words)

# defaultdict for grouping
groups = defaultdict(list)

# deque for queue operations
queue = deque(maxlen=10)

# namedtuple for structured data
Point = namedtuple('Point', ['x', 'y'])

# ChainMap for layered lookups
configs = ChainMap(user_config, default_config)
```

### Performance Considerations
```python
# Use deque for queue operations (O(1))
queue = deque()
queue.append(1)      # Fast
queue.popleft()      # Fast

# Don't use list for queue operations
lst = []
lst.append(1)        # Fast
lst.pop(0)          # Slow (O(n))
```

## Common Patterns

### Counting with Counter
```python
# Most common words
def most_common_words(text, n=10):
    words = text.lower().split()
    return Counter(words).most_common(n)

# Finding duplicates
def find_duplicates(items):
    counts = Counter(items)
    return {item: count for item, count in counts.items() if count > 1}
```

### Multi-level Defaultdict
```python
# Creating nested structure
def tree():
    return defaultdict(tree)

filesystem = tree()
filesystem["home"]["user"]["documents"] = "content"
```

### Priority Queue with deque
```python
class PriorityQueue:
    def __init__(self):
        self.queues = defaultdict(deque)
        
    def add(self, item, priority=0):
        self.queues[priority].append(item)
        
    def get(self):
        if not self.queues:
            raise IndexError("queue is empty")
        highest_priority = max(self.queues.keys())
        return self.queues[highest_priority].popleft()
```

## Exercises

1. Create a frequency analyzer using Counter
2. Implement a cache with OrderedDict
3. Build a directory tree structure using defaultdict
4. Create a command history feature using deque
5. Implement a configuration system using ChainMap