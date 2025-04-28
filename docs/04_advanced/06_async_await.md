# Python Async/Await

## Basic Concepts

### Coroutines
```python
import asyncio

async def hello():
    """Simple coroutine"""
    print("Hello")
    await asyncio.sleep(1)
    print("World")

# Running a coroutine
async def main():
    await hello()

asyncio.run(main())
```

### Tasks
```python
async def count_up(name, delay):
    """Count up with delay"""
    for i in range(3):
        print(f"{name}: {i}")
        await asyncio.sleep(delay)
    return f"{name} finished counting"

async def run_tasks():
    # Create tasks for concurrent execution
    task1 = asyncio.create_task(count_up("Counter 1", 1))
    task2 = asyncio.create_task(count_up("Counter 2", 0.5))
    
    # Wait for both tasks to complete
    results = await asyncio.gather(task1, task2)
    print(results)

# Run multiple tasks concurrently
asyncio.run(run_tasks())
```

## Advanced Features

### Async Context Managers
```python
class AsyncResource:
    """Example of async context manager"""
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)  # Simulate async initialization
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(0.5)  # Simulate async cleanup
    
    async def do_something(self):
        print("Using resource")
        await asyncio.sleep(0.5)

async def use_resource():
    async with AsyncResource() as resource:
        await resource.do_something()

asyncio.run(use_resource())
```

### Async Iterators
```python
class AsyncCounter:
    """Example of async iterator"""
    def __init__(self, limit):
        self.limit = limit
        self.counter = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.counter >= self.limit:
            raise StopAsyncIteration
        self.counter += 1
        await asyncio.sleep(0.1)
        return self.counter

async def use_async_iterator():
    async for number in AsyncCounter(5):
        print(f"Number: {number}")

asyncio.run(use_async_iterator())
```

### Event Loop Control
```python
async def background_task():
    """Task running in background"""
    while True:
        print("Background task running")
        await asyncio.sleep(2)

async def main_task():
    """Main application task"""
    task = asyncio.create_task(background_task())
    
    # Run for 5 seconds
    try:
        await asyncio.sleep(5)
    finally:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            print("Background task was cancelled")

# Run with custom event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    loop.run_until_complete(main_task())
finally:
    loop.close()
```

## Practical Applications

### Async HTTP Client
```python
import aiohttp
import asyncio

async def fetch_url(session, url):
    """Fetch single URL asynchronously"""
    async with session.get(url) as response:
        return await response.text()

async def fetch_multiple_urls(urls):
    """Fetch multiple URLs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

async def main():
    urls = [
        'http://example.com',
        'http://example.org',
        'http://example.net'
    ]
    results = await fetch_multiple_urls(urls)
    for url, html in zip(urls, results):
        print(f"Got {len(html)} bytes from {url}")

# Run async HTTP requests
asyncio.run(main())
```

### Async Database Operations
```python
import asyncpg

async def create_pool():
    """Create connection pool"""
    return await asyncpg.create_pool(
        user='user',
        password='password',
        database='database',
        host='localhost'
    )

async def fetch_users(pool):
    """Fetch users from database"""
    async with pool.acquire() as connection:
        return await connection.fetch('SELECT * FROM users')

async def insert_user(pool, name, email):
    """Insert user into database"""
    async with pool.acquire() as connection:
        return await connection.execute(
            'INSERT INTO users(name, email) VALUES($1, $2)',
            name, email
        )

async def main():
    # Create connection pool
    pool = await create_pool()
    try:
        # Insert user
        await insert_user(pool, 'John', 'john@example.com')
        
        # Fetch users
        users = await fetch_users(pool)
        for user in users:
            print(f"User: {user['name']}, Email: {user['email']}")
    finally:
        await pool.close()

# Run database operations
asyncio.run(main())
```

### Async File Operations
```python
import aiofiles

async def read_file(filename):
    """Read file asynchronously"""
    async with aiofiles.open(filename, mode='r') as file:
        content = await file.read()
        return content

async def write_file(filename, content):
    """Write file asynchronously"""
    async with aiofiles.open(filename, mode='w') as file:
        await file.write(content)

async def process_files():
    # Write file
    await write_file('test.txt', 'Hello, World!')
    
    # Read file
    content = await read_file('test.txt')
    print(f"File content: {content}")

# Run file operations
asyncio.run(process_files())
```

## Best Practices

### Error Handling
```python
async def fetch_with_timeout(url, timeout=5):
    """Fetch URL with timeout and error handling"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await asyncio.wait_for(
                    response.text(),
                    timeout=timeout
                )
    except asyncio.TimeoutError:
        print(f"Timeout fetching {url}")
    except aiohttp.ClientError as e:
        print(f"Error fetching {url}: {e}")
    return None

async def main():
    urls = [
        'http://example.com',
        'http://nonexistent.com',
        'http://slow.example.com'
    ]
    tasks = [fetch_with_timeout(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for url, result in zip(urls, results):
        if isinstance(result, Exception):
            print(f"Failed to fetch {url}: {result}")
        elif result:
            print(f"Successfully fetched {url}")
```

### Resource Management
```python
class AsyncPool:
    """Example of async resource pool"""
    def __init__(self, size):
        self.size = size
        self._semaphore = asyncio.Semaphore(size)
        self._resources = set()
    
    async def acquire(self):
        await self._semaphore.acquire()
        resource = object()  # Create resource
        self._resources.add(resource)
        return resource
    
    async def release(self, resource):
        self._resources.remove(resource)
        self._semaphore.release()
    
    async def __aenter__(self):
        return await self.acquire()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.release(exc_val)

async def use_pool():
    pool = AsyncPool(3)
    async with pool as resource:
        # Use resource
        await asyncio.sleep(1)
```

## Common Patterns

### Producer-Consumer
```python
async def producer(queue):
    """Produce items and put them in queue"""
    for i in range(5):
        await queue.put(f"Item {i}")
        await asyncio.sleep(1)
    await queue.put(None)  # Signal end

async def consumer(queue):
    """Consume items from queue"""
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Processing {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    await asyncio.gather(producer_task, consumer_task)
```

### Throttling
```python
class Throttler:
    """Rate limiter for async operations"""
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self._lock = asyncio.Lock()
        self._last_update = time.monotonic()
    
    async def acquire(self):
        async with self._lock:
            now = time.monotonic()
            time_passed = now - self._last_update
            self.tokens = min(
                self.rate_limit,
                self.tokens + time_passed * self.rate_limit
            )
            
            if self.tokens < 1:
                wait_time = (1 - self.tokens) / self.rate_limit
                await asyncio.sleep(wait_time)
                self.tokens = 1
            
            self.tokens -= 1
            self._last_update = now

async def throttled_operation(throttler, operation_id):
    await throttler.acquire()
    print(f"Executing operation {operation_id}")
```

## Exercises

1. Create an async web scraper that respects rate limits
2. Implement an async connection pool with retry logic
3. Create an async task scheduler with priorities
4. Implement an async pub/sub system
5. Create an async file processing pipeline