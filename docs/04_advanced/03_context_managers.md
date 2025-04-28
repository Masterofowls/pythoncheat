# Python Context Managers

## Basic Context Managers

### Using with Statement
```python
# Basic file handling with context manager
with open('example.txt', 'w') as file:
    file.write('Hello, World!')
# File is automatically closed after the block

# Multiple context managers
with open('input.txt') as in_file, open('output.txt', 'w') as out_file:
    content = in_file.read()
    out_file.write(content.upper())
```

### Class-based Context Managers
```python
class DatabaseConnection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connection = None
    
    def __enter__(self):
        """Set up the context and return the resource"""
        print(f"Connecting to {self.host}:{self.port}")
        self.connection = {"host": self.host, "port": self.port}
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the context"""
        print("Closing database connection")
        self.connection = None
        # Return True to suppress exceptions, False to propagate them
        return False

# Using the context manager
with DatabaseConnection('localhost', 5432) as conn:
    print(f"Connected to {conn['host']}")
```

## Function-based Context Managers

### Using contextmanager Decorator
```python
from contextlib import contextmanager
import time

@contextmanager
def timer():
    """Measure execution time of a code block"""
    start = time.time()
    yield
    end = time.time()
    print(f"Execution took {end - start:.2f} seconds")

# Using the timer
with timer():
    # Some time-consuming operation
    time.sleep(1)
```

### Generator-based Context Manager
```python
@contextmanager
def tempfile(content):
    """Create a temporary file with given content"""
    import os
    
    filename = 'temp.txt'
    try:
        with open(filename, 'w') as f:
            f.write(content)
        yield filename
    finally:
        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

# Using the temporary file
with tempfile("Hello, World!") as filename:
    with open(filename) as f:
        content = f.read()
        print(content)
# File is automatically deleted after the block
```

## Advanced Context Managers

### Context Managers with Arguments
```python
class IndentedWriter:
    def __init__(self, filename, indent_level=0):
        self.filename = filename
        self.indent_level = indent_level
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
    
    def write(self, text):
        indent = "    " * self.indent_level
        self.file.write(f"{indent}{text}\n")
    
    @contextmanager
    def indented(self):
        """Temporarily increase indentation level"""
        self.indent_level += 1
        yield
        self.indent_level -= 1

# Using nested context managers
with IndentedWriter('nested.txt') as writer:
    writer.write('Level 0')
    with writer.indented():
        writer.write('Level 1')
        with writer.indented():
            writer.write('Level 2')
```

### Exception Handling
```python
class Transaction:
    def __init__(self):
        self.operations = []
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            # No exception occurred, commit the transaction
            print("Committing transaction")
            return True
        else:
            # Exception occurred, rollback
            print(f"Rolling back due to {exc_type.__name__}: {exc_val}")
            self.operations.clear()
            return False  # Re-raise the exception
    
    def add_operation(self, op):
        self.operations.append(op)

# Using transaction with error handling
try:
    with Transaction() as tx:
        tx.add_operation("Save user")
        tx.add_operation("Update profile")
        raise ValueError("Something went wrong")
except ValueError:
    print("Transaction was rolled back")
```

## Practical Examples

### Resource Management
```python
class Lock:
    def __init__(self):
        self._locked = False
    
    def acquire(self):
        self._locked = True
    
    def release(self):
        self._locked = False
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# Using lock as context manager
lock = Lock()
with lock:
    # Critical section
    print("Executing with lock")
# Lock is automatically released
```

### Managing Multiple Resources
```python
@contextmanager
def resource_manager(*resources):
    """Manage multiple resources in correct order"""
    acquired = []
    try:
        for resource in resources:
            resource.acquire()
            acquired.append(resource)
        yield
    finally:
        # Release in reverse order
        for resource in reversed(acquired):
            resource.release()

# Using multiple resources
lock1, lock2 = Lock(), Lock()
with resource_manager(lock1, lock2):
    print("Using both resources")
```

### Redirect Output
```python
from contextlib import redirect_stdout, redirect_stderr
import sys
from io import StringIO

def process_with_output():
    print("Standard output")
    print("Error message", file=sys.stderr)

# Capture output
output = StringIO()
error = StringIO()

with redirect_stdout(output), redirect_stderr(error):
    process_with_output()

print("Captured output:", output.getvalue())
print("Captured errors:", error.getvalue())
```

## Built-in Context Managers

### suppress
```python
from contextlib import suppress

# Instead of try-except with pass
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')
```

### closing
```python
from contextlib import closing
from urllib.request import urlopen

# Automatically close the connection
with closing(urlopen('http://example.com')) as page:
    content = page.read()
```

### nullcontext
```python
from contextlib import nullcontext

def process_file(filename, file_obj=None):
    # Use provided file object or open new file
    cm = file_obj if file_obj is not None else open(filename)
    with cm:
        return cm.read()

# Using nullcontext for optional context management
with nullcontext() as nothing:
    print("This block doesn't need context management")
```

## Best Practices

### Proper Resource Management
```python
class Resource:
    def __init__(self, name):
        self.name = name
        self.acquired = False
    
    def acquire(self):
        if self.acquired:
            raise RuntimeError("Resource already acquired")
        print(f"Acquiring {self.name}")
        self.acquired = True
    
    def release(self):
        if not self.acquired:
            raise RuntimeError("Resource not acquired")
        print(f"Releasing {self.name}")
        self.acquired = False
    
    def __enter__(self):
        self.acquire()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# Using resource properly
with Resource("database") as db:
    print("Using database")
```

### Reentrant Context Managers
```python
class ReentrantLock:
    def __init__(self):
        self._lock = 0
    
    def __enter__(self):
        self._lock += 1
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._lock -= 1

# Can be nested safely
lock = ReentrantLock()
with lock:
    print("First level")
    with lock:
        print("Second level")
```

## Exercises

1. Create a context manager for measuring memory usage
2. Implement a context manager for changing working directory
3. Create a context manager for temporary environment variables
4. Implement a connection pool context manager
5. Create a context manager for logging function entry and exit