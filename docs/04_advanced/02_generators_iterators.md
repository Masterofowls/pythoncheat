# Python Generators and Iterators

## Iterators

### Basic Iterator Protocol
```python
class CountUp:
    """Simple iterator that counts up from a start number"""
    def __init__(self, start, end):
        self.current = start
        self.end = end
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current > self.end:
            raise StopIteration
        current = self.current
        self.current += 1
        return current

# Using the iterator
counter = CountUp(1, 3)
for num in counter:
    print(num)  # Prints 1, 2, 3
```

### Custom Sequence Iterator
```python
class Fibonacci:
    """Iterator that generates Fibonacci sequence"""
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.a = 0
        self.b = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        
        if self.count == 0:
            self.count += 1
            return self.a
        elif self.count == 1:
            self.count += 1
            return self.b
        
        result = self.a + self.b
        self.a, self.b = self.b, result
        self.count += 1
        return result

# Using Fibonacci iterator
fib = Fibonacci(5)
print(list(fib))  # [0, 1, 1, 2, 3]
```

## Generators

### Basic Generator Functions
```python
def count_up(start, end):
    """Generator function that counts up from start to end"""
    current = start
    while current <= end:
        yield current
        current += 1

# Using the generator
for num in count_up(1, 3):
    print(num)  # Prints 1, 2, 3

# Generator expression
squares = (x**2 for x in range(5))
print(list(squares))  # [0, 1, 4, 9, 16]
```

### Generator with State
```python
def stateful_generator(start=0):
    """Generator that maintains state between yields"""
    count = start
    while True:
        # receive value from send()
        val = yield count
        if val is not None:
            count = val
        else:
            count += 1

# Using stateful generator
gen = stateful_generator(1)
print(next(gen))    # 1
print(next(gen))    # 2
print(gen.send(10)) # 10
print(next(gen))    # 11
```

### Infinite Generators
```python
def fibonacci_infinite():
    """Infinite generator for Fibonacci sequence"""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Using infinite generator with limit
def take(n, iterator):
    """Take first n items from iterator"""
    return [next(iterator) for _ in range(n)]

fib = fibonacci_infinite()
print(take(10, fib))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

## Advanced Generator Features

### Generator Methods
```python
def number_generator():
    """Generator demonstrating .send(), .throw(), and .close()"""
    try:
        start = yield "Ready to start!"
        print(f"Started with {start}")
        
        while True:
            try:
                received = yield start
                if received is not None:
                    start = received
                else:
                    start += 1
            except ValueError as e:
                start = yield f"Caught error: {e}"
    finally:
        print("Generator is closing")

# Using generator methods
gen = number_generator()
print(next(gen))          # Ready to start!
print(gen.send(10))       # Started with 10, returns 10
print(next(gen))          # 11
print(gen.throw(ValueError("Invalid number")))  # Caught error: Invalid number
gen.close()              # Generator is closing
```

### Subgenerators with yield from
```python
def sub_gen(start, end):
    """Subgenerator that yields a range of numbers"""
    for i in range(start, end):
        yield i

def main_gen(ranges):
    """Main generator that delegates to subgenerators"""
    for start, end in ranges:
        yield from sub_gen(start, end)
        yield "---"  # Separator between ranges

# Using yield from
ranges = [(1, 4), (5, 7)]
for item in main_gen(ranges):
    print(item)  # 1, 2, 3, ---, 5, 6, ---
```

## Generator Patterns

### Pipeline with Generators
```python
def read_data():
    """Generate raw data"""
    data = [1, 2, 3, 4, 5]
    for item in data:
        yield item

def filter_even(numbers):
    """Filter even numbers"""
    for num in numbers:
        if num % 2 == 0:
            yield num

def multiply_by_two(numbers):
    """Multiply each number by two"""
    for num in numbers:
        yield num * 2

# Creating pipeline
def pipeline():
    return multiply_by_two(filter_even(read_data()))

print(list(pipeline()))  # [4, 8]
```

### Context Manager with Generator
```python
from contextlib import contextmanager

@contextmanager
def managed_file(filename):
    """File context manager implemented as generator"""
    try:
        f = open(filename, 'w')
        yield f
    finally:
        f.close()

# Using the context manager
with managed_file('test.txt') as f:
    f.write('Hello, World!')
```

### Lazy Evaluation
```python
def compute_expensive_values():
    """Generator for expensive computations"""
    cache = {}
    
    for i in range(10):
        if i in cache:
            result = cache[i]
        else:
            # Simulate expensive computation
            result = i ** 2
            cache[i] = result
        yield result

# Values are computed only when needed
values = compute_expensive_values()
print(next(values))  # Computes and returns first value
print(next(values))  # Computes and returns second value
```

## Best Practices

### Memory Efficient Processing
```python
def process_large_file(filename):
    """Process file line by line instead of loading entirely"""
    with open(filename) as f:
        for line in f:
            # Process line
            yield line.strip().upper()

# Using the generator
for processed_line in process_large_file('large_file.txt'):
    print(processed_line)
```

### Generator Expression vs List Comprehension
```python
# List comprehension - creates full list in memory
squares_list = [x**2 for x in range(1000000)]

# Generator expression - creates values on demand
squares_gen = (x**2 for x in range(1000000))

# Memory efficient sum using generator
total = sum(squares_gen)
```

## Common Patterns

### Batch Processing
```python
def batch_generator(data, batch_size):
    """Generate data in batches"""
    for i in range(0, len(data), batch_size):
        yield data[i:i + batch_size]

# Process data in batches
data = list(range(10))
for batch in batch_generator(data, 3):
    print(f"Processing batch: {batch}")
```

### Event Stream
```python
def event_stream():
    """Simulate event stream"""
    import time
    events = []
    while True:
        # Check for new events
        while events:
            yield events.pop(0)
        time.sleep(0.1)

def handle_events():
    stream = event_stream()
    for event in stream:
        print(f"Handling event: {event}")
```

## Exercises

1. Create a generator that yields prime numbers up to a given limit
2. Implement a generator-based solution for reading and processing large CSV files
3. Create a pipeline of generators for text processing
4. Implement a generator that simulates a task scheduler
5. Create a memory-efficient data transformation pipeline using generators