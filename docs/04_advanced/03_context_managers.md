# Python Context Managers

## Basic Context Managers

### Class-based Context Managers
```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, exc_tb):
        if self.file:
            self.file.close()
        # Return True to suppress exception
        return False

# Using the context manager
with FileManager('example.txt', 'w') as f:
    f.write('Hello, World!')
```

### Function-based Context Managers
```python
from contextlib import contextmanager

@contextmanager
def file_manager(filename, mode):
    try:
        f = open(filename, mode)
        yield f
    finally:
        f.close()

# Using the context manager
with file_manager('example.txt', 'w') as f:
    f.write('Hello, World!')
```

## Resource Management

### Database Connections
```python
class DatabaseConnection:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.conn = None
    
    def __enter__(self):
        self.conn = connect_to_db(self.host, 
                                self.user,
                                self.password)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

# Using database connection
with DatabaseConnection('localhost', 'user', 'pass') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
```

### Thread Lock Management
```python
from threading import Lock

@contextmanager
def managed_lock(lock):
    """Context manager for thread locks"""
    try:
        lock.acquire()
        yield
    finally:
        lock.release()

# Using lock manager
lock = Lock()
with managed_lock(lock):
    # Critical section
    process_shared_resource()
```

## Advanced Context Managers

### Nested Context Managers
```python
class Transaction:
    def __init__(self, connection):
        self.conn = connection
    
    def __enter__(self):
        self.conn.begin()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

# Nested usage
with DatabaseConnection('localhost', 'user', 'pass') as conn:
    with Transaction(conn):
        cursor = conn.cursor()
        cursor.execute('UPDATE users SET active = 1')
```

### Context Manager with Exception Handling
```python
class ErrorHandler:
    def __init__(self, error_log):
        self.error_log = error_log
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            with open(self.error_log, 'a') as f:
                f.write(f"Error: {exc_val}\n")
            return True  # Suppress exception
        return False

# Using error handler
with ErrorHandler('errors.log'):
    # This error will be logged but not raised
    raise ValueError("Something went wrong")
```

## Contextlib Utilities

### Closing Resources
```python
from contextlib import closing

class Resource:
    def close(self):
        print("Resource cleaned up")

# Using closing
with closing(Resource()) as r:
    # Resource will be closed after the block
    pass
```

### Suppress Exceptions
```python
from contextlib import suppress

# Suppress specific exceptions
with suppress(FileNotFoundError):
    os.remove('nonexistent_file.txt')

# Multiple exceptions
with suppress(KeyError, AttributeError):
    value = data['key'].attribute
```

### Redirecting Output
```python
from contextlib import redirect_stdout, redirect_stderr
import sys

# Redirect stdout to file
with open('output.log', 'w') as f:
    with redirect_stdout(f):
        print("This goes to the file")

# Redirect stderr
with open('error.log', 'w') as f:
    with redirect_stderr(f):
        sys.stderr.write("Error message")
```

## Best Practices

### Proper Resource Cleanup
```python
class ResourceManager:
    def __init__(self):
        self.resource = None
    
    def __enter__(self):
        try:
            self.resource = self.acquire_resource()
            return self.resource
        except Exception:
            # Clean up if acquisition fails
            if self.resource:
                self.release_resource()
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Always clean up, even if exception occurs
        if self.resource:
            self.release_resource()
```

### Context Manager Composition
```python
@contextmanager
def combined_context(*managers):
    """Combine multiple context managers"""
    with ExitStack() as stack:
        yield tuple(stack.enter_context(mgr) for mgr in managers)

# Using multiple contexts
with combined_context(
    open('input.txt'),
    open('output.txt', 'w')
) as (in_file, out_file):
    out_file.write(in_file.read().upper())
```

## Common Patterns

### Temporary State
```python
@contextmanager
def temporary_attribute(obj, name, value):
    """Temporarily set an attribute"""
    old_value = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old_value)

# Usage
class Config:
    debug = False

config = Config()
with temporary_attribute(config, 'debug', True):
    # debug is True here
    run_debug_code()
# debug is False again
```

### Timer Context
```python
@contextmanager
def timer(description):
    """Measure execution time of a code block"""
    from time import time
    start = time()
    yield
    elapsed = time() - start
    print(f"{description}: {elapsed:.2f} seconds")

# Usage
with timer("Processing data"):
    process_large_dataset()
```

## Exercises

1. Create a context manager for managing temporary files
2. Implement a context manager for database transactions
3. Build a context manager for changing working directory
4. Create a context manager for measuring memory usage
5. Implement a context manager for temporary environment variables