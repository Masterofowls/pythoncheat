# Python Generators and Iterators

## Iterators

### Basic Iterator Protocol
```python
class Counter:
    """Simple iterator that counts up to n"""
    def __init__(self, n):
        self.n = n
        self.current = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.n:
            raise StopIteration
        self.current += 1
        return self.current

# Using the iterator
counter = Counter(3)
for num in counter:
    print(num)  # Prints 1, 2, 3
```

### Custom Iterator Class
```python
class FibonacciIterator:
    """Iterator that generates Fibonacci numbers"""
    def __init__(self, max_numbers):
        self.max_numbers = max_numbers
        self.current = 0
        self.a, self.b = 0, 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= self.max_numbers:
            raise StopIteration
        
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        self.current += 1
        return result

# Using FibonacciIterator
fib = FibonacciIterator(5)
print(list(fib))  # [0, 1, 1, 2, 3]
```

## Generators

### Basic Generator Functions
```python
def countdown(n):
    """Generator that counts down from n to 1"""
    while n > 0:
        yield n
        n -= 1

# Using the generator
for num in countdown(3):
    print(num)  # Prints 3, 2, 1

def fibonacci(max_numbers):
    """Generator for Fibonacci numbers"""
    a, b = 0, 1
    count = 0
    while count < max_numbers:
        yield a
        a, b = b, a + b
        count += 1

# Using fibonacci generator
print(list(fibonacci(5)))  # [0, 1, 1, 2, 3]
```

### Generator Expressions
```python
# Generator expression
squares = (x**2 for x in range(5))

# Comparing with list comprehension
squares_list = [x**2 for x in range(5)]  # Creates list in memory
squares_gen = (x**2 for x in range(5))   # Creates generator object

# Memory efficient processing of large sequences
sum(x**2 for x in range(1000000))
```

## Advanced Generator Features

### Send and Throw
```python
def counter():
    """Generator that can receive values"""
    count = 0
    while True:
        val = yield count
        if val is not None:
            count = val
        else:
            count += 1

# Using send
c = counter()
print(next(c))      # 0
print(c.send(10))   # 10
print(next(c))      # 11

def error_handler():
    """Generator that can handle exceptions"""
    while True:
        try:
            x = yield
        except ValueError:
            print("Caught ValueError!")
        else:
            print(f"Received: {x}")

# Using throw
h = error_handler()
next(h)  # Prime the generator
h.send(1)          # Received: 1
h.throw(ValueError)  # Caught ValueError!
```

### Subgenerators (yield from)
```python
def sub_gen():
    yield 1
    yield 2
    yield 3

def main_gen():
    yield 'a'
    yield from sub_gen()
    yield 'b'

# Using yield from
for item in main_gen():
    print(item)  # Prints: a, 1, 2, 3, b
```

## Infinite Generators

### Infinite Sequences
```python
def infinite_counter(start=0):
    """Infinite counting generator"""
    num = start
    while True:
        yield num
        num += 1

# Using itertools.islice to limit infinite generator
from itertools import islice
first_five = list(islice(infinite_counter(), 5))
print(first_five)  # [0, 1, 2, 3, 4]

def primes():
    """Infinite generator for prime numbers"""
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    n = 2
    while True:
        if is_prime(n):
            yield n
        n += 1

# Get first 5 primes
print(list(islice(primes(), 5)))  # [2, 3, 5, 7, 11]
```

## Generator Pipelines

### Building Data Pipelines
```python
def read_lines(file):
    """Generator that reads lines from file"""
    with open(file) as f:
        for line in f:
            yield line.strip()

def grep(pattern, lines):
    """Generator that filters lines matching pattern"""
    for line in lines:
        if pattern in line:
            yield line

def uppercase(lines):
    """Generator that converts lines to uppercase"""
    for line in lines:
        yield line.upper()

# Composing generators
def process_log(file):
    lines = read_lines(file)
    errors = grep('ERROR', lines)
    upper_errors = uppercase(errors)
    return upper_errors

# Usage
# for line in process_log('app.log'):
#     print(line)
```

## Memory-Efficient Processing

### Processing Large Files
```python
def process_large_file(filename):
    """Memory-efficient file processing"""
    def read_chunks(file, chunk_size=1024):
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            yield chunk
    
    with open(filename, 'rb') as f:
        for chunk in read_chunks(f):
            # Process chunk here
            pass

def csv_reader(file_name):
    """Memory-efficient CSV reader"""
    for row in open(file_name):
        yield row.rstrip().split(',')
```

## Best Practices

### Generator vs List
```python
# Memory inefficient
def get_all_users():
    users = []
    for user in database.query():
        users.append(process_user(user))
    return users

# Memory efficient
def get_all_users():
    for user in database.query():
        yield process_user(user)

# Using generators for large datasets
def process_large_dataset():
    data = get_all_users()  # Returns generator
    processed = (process(item) for item in data)  # Another generator
    for result in processed:  # Process one item at a time
        save_result(result)
```

### Error Handling
```python
def safe_generator():
    """Generator with proper cleanup"""
    resource = acquire_resource()
    try:
        for item in resource:
            yield item
    finally:
        resource.cleanup()

def with_retry(generator, max_attempts=3):
    """Wrapper for generators with retry logic"""
    attempt = 0
    while attempt < max_attempts:
        try:
            yield from generator
            break
        except Exception as e:
            attempt += 1
            if attempt == max_attempts:
                raise e
```

## Common Patterns

### Batch Processing
```python
def batch_items(items, batch_size=100):
    """Generator that yields batches of items"""
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

# Usage
items = range(350)
for batch in batch_items(items, 100):
    process_batch(batch)
```

### State Machines
```python
def parser_fsm():
    """Generator-based finite state machine"""
    state = 'START'
    while True:
        char = yield
        if state == 'START':
            if char == '{':
                state = 'OPEN_BRACE'
            elif char == '[':
                state = 'OPEN_BRACKET'
        elif state == 'OPEN_BRACE':
            if char == '}':
                state = 'START'
        elif state == 'OPEN_BRACKET':
            if char == ']':
                state = 'START'
```

## Exercises

1. Create a generator that yields all permutations of a sequence
2. Implement a generator-based pipeline for processing log files
3. Build a memory-efficient pagination system using generators
4. Create a generator that implements the merge step of merge sort
5. Design a generator-based task scheduler