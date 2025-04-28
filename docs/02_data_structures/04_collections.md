# Python Collections Module

## Counter

### Basic Counter Usage
```python
from collections import Counter

# Creating Counters
word_counts = Counter(['apple', 'banana', 'apple', 'cherry'])
char_counts = Counter('mississippi')
dict_counter = Counter({'a': 4, 'b': 2})

# Counting methods
text = "hello world"
counts = Counter(text)
print(counts)  # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ' ': 1, 'w': 1, 'r': 1, 'd': 1})
```

### Counter Operations
```python
c1 = Counter(['a', 'b', 'b', 'c'])
c2 = Counter(['b', 'b', 'c', 'd'])

# Addition
combined = c1 + c2  # Counter({'b': 4, 'c': 2, 'a': 1, 'd': 1})

# Subtraction
diff = c1 - c2     # Counter({'a': 1})

# Intersection
common = c1 & c2   # Counter({'b': 2, 'c': 1})

# Union
all_counts = c1 | c2  # Counter({'b': 2, 'c': 1, 'a': 1, 'd': 1})

# Most common elements
top_3 = counts.most_common(3)
```

## defaultdict

### Basic defaultdict Usage
```python
from collections import defaultdict

# Integer default
int_dict = defaultdict(int)
int_dict['a'] += 1  # No KeyError

# List default
list_dict = defaultdict(list)
list_dict['colors'].append('red')  # No KeyError

# Set default
set_dict = defaultdict(set)
set_dict['numbers'].add(42)  # No KeyError
```

### Common Applications
```python
# Grouping
def group_by_length(words):
    groups = defaultdict(list)
    for word in words:
        groups[len(word)].append(word)
    return dict(groups)

# Counting
def count_items(items):
    counts = defaultdict(int)
    for item in items:
        counts[item] += 1
    return dict(counts)

# Building graphs
def build_graph(edges):
    graph = defaultdict(set)
    for start, end in edges:
        graph[start].add(end)
        graph[end].add(start)
    return graph
```

## deque (Double-Ended Queue)

### Basic deque Usage
```python
from collections import deque

# Creating deques
d = deque()
d = deque([1, 2, 3])
d = deque('hello')
d = deque(maxlen=3)  # Fixed-length deque

# Basic operations
d.append(4)        # Add to right
d.appendleft(0)    # Add to left
d.pop()            # Remove from right
d.popleft()        # Remove from left
d.extend([4, 5])   # Extend on right
d.extendleft([0, -1])  # Extend on left
```

### Advanced deque Operations
```python
d = deque([1, 2, 3, 4, 5])

# Rotation
d.rotate(2)    # [4, 5, 1, 2, 3]
d.rotate(-2)   # [1, 2, 3, 4, 5]

# Clearing
d.clear()

# Counting
d = deque([1, 2, 2, 3, 2])
count = d.count(2)  # 3

# Reversing
d.reverse()
```

## namedtuple

### Basic namedtuple Usage
```python
from collections import namedtuple

# Creating named tuples
Point = namedtuple('Point', ['x', 'y'])
Person = namedtuple('Person', 'name age city')

# Creating instances
p = Point(11, y=22)
person = Person('John', 30, 'New York')

# Accessing fields
print(p.x, p.y)
print(person.name, person.age, person.city)
```

### Advanced namedtuple Features
```python
# Default values
Employee = namedtuple('Employee', ['name', 'salary'], defaults=['Unknown', 0])
e = Employee()  # Employee(name='Unknown', salary=0)

# Converting to dictionary
person_dict = person._asdict()

# Creating new instance with updates
updated_person = person._replace(age=31)

# Field names
print(Person._fields)  # ('name', 'age', 'city')
```

## ChainMap

### Basic ChainMap Usage
```python
from collections import ChainMap

# Creating ChainMaps
defaults = {'theme': 'dark', 'language': 'en'}
user_settings = {'language': 'fr'}
combined = ChainMap(user_settings, defaults)

# Accessing values
print(combined['theme'])     # 'dark' from defaults
print(combined['language'])  # 'fr' from user_settings
```

### ChainMap Operations
```python
# Adding new mappings
local = {'debug': True}
settings = ChainMap(local, user_settings, defaults)

# Updating values
settings['theme'] = 'light'  # Only updates first mapping

# Creating new child
child = settings.new_child()
child['theme'] = 'custom'
```

## OrderedDict

### Basic OrderedDict Usage
```python
from collections import OrderedDict

# Creating ordered dictionaries
od = OrderedDict()
od['first'] = 1
od['second'] = 2
od['third'] = 3

# Comparing with regular dict (Python 3.7+)
regular_dict = {'a': 1, 'b': 2}  # Also ordered by insertion
ordered_dict = OrderedDict([('a', 1), ('b', 2)])
```

### OrderedDict Operations
```python
# Moving items
od.move_to_end('first')     # Move to last
od.move_to_end('first', last=False)  # Move to first

# Popping items
last = od.popitem()         # Remove last item
first = od.popitem(last=False)  # Remove first item
```

## Best Practices

### Choosing the Right Collection
```python
# Use Counter for counting
def word_frequency(text):
    return Counter(text.split())

# Use defaultdict for grouping
def group_by_category(items):
    groups = defaultdict(list)
    for item, category in items:
        groups[category].append(item)
    return dict(groups)

# Use deque for FIFO/LIFO queues
def process_queue(items, maxlen=None):
    queue = deque(items, maxlen=maxlen)
    while queue:
        item = queue.popleft()
        process(item)
```

### Performance Considerations
```python
# deque vs list
from timeit import timeit

# deque is faster for append/pop from both ends
deque_time = timeit('d.appendleft(0)', 'from collections import deque; d=deque()')
list_time = timeit('l.insert(0, 0)', 'l=[]')

# Counter vs manual counting
def count_manual(items):
    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1
    return counts

def count_with_counter(items):
    return Counter(items)
```

## Common Patterns

### Event History
```python
class EventHistory:
    def __init__(self, maxlen=1000):
        self.events = deque(maxlen=maxlen)
    
    def add_event(self, event):
        self.events.append(event)
    
    def get_recent(self, n):
        return list(itertools.islice(self.events, len(self.events) - n, None))
```

### Multi-level Settings
```python
class Settings:
    def __init__(self):
        self.maps = ChainMap()
    
    def push_layer(self, mapping):
        self.maps = self.maps.new_child(mapping)
    
    def pop_layer(self):
        return self.maps.parents
```

### Frequency Analysis
```python
def analyze_text(text):
    words = text.lower().split()
    word_freq = Counter(words)
    
    return {
        'most_common': word_freq.most_common(5),
        'unique_words': len(word_freq),
        'total_words': sum(word_freq.values())
    }
```

## Exercises

1. Implement a cache with a maximum size using OrderedDict
2. Create a breadth-first search using deque
3. Build a frequency-based text analyzer using Counter
4. Implement a multi-level configuration system using ChainMap
5. Create a circular buffer using deque with maxlen