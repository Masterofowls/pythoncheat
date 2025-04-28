# Python Async/Await

## Basic Concepts

### Coroutines
```python
async def my_coroutine():
    print("Start")
    await asyncio.sleep(1)
    print("End")

# Running a coroutine
import asyncio
asyncio.run(my_coroutine())
```

### Tasks
```python
async def main():
    # Create and schedule a task
    task = asyncio.create_task(my_coroutine())
    
    # Wait for task completion
    await task

async def long_operation():
    await asyncio.sleep(2)
    return "Done"

# Running multiple tasks
async def run_tasks():
    tasks = [
        asyncio.create_task(long_operation())
        for _ in range(3)
    ]
    results = await asyncio.gather(*tasks)
    print(results)  # ['Done', 'Done', 'Done']
```

## Async Context Managers

### Basic Context Manager
```python
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(1)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(1)

async def use_resource():
    async with AsyncResource() as res:
        print("Using resource")
```

### Database Connection
```python
class AsyncDatabase:
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
    
    async def connect(self):
        await asyncio.sleep(1)  # Simulate connection
        print("Connected to database")
    
    async def disconnect(self):
        await asyncio.sleep(1)  # Simulate disconnection
        print("Disconnected from database")
    
    async def query(self, sql):
        await asyncio.sleep(0.5)  # Simulate query
        return f"Result of {sql}"
```

## Async Iterators

### Basic Iterator
```python
class AsyncCounter:
    def __init__(self, stop):
        self.current = 0
        self.stop = stop
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.current >= self.stop:
            raise StopAsyncIteration
        
        self.current += 1
        await asyncio.sleep(0.1)
        return self.current

async def use_counter():
    async for i in AsyncCounter(3):
        print(i)  # 1, 2, 3
```

### Async Generator
```python
async def async_range(stop):
    for i in range(stop):
        await asyncio.sleep(0.1)
        yield i

async def use_generator():
    async for i in async_range(3):
        print(i)  # 0, 1, 2
```

## Error Handling

### Try/Except with Async
```python
async def might_fail():
    await asyncio.sleep(1)
    raise ValueError("Something went wrong")

async def handle_errors():
    try:
        await might_fail()
    except ValueError as e:
        print(f"Caught error: {e}")
    finally:
        print("Cleanup")
```

### Timeout Handling
```python
async def long_task():
    await asyncio.sleep(5)
    return "Done"

async def with_timeout():
    try:
        async with asyncio.timeout(2):
            result = await long_task()
            print(result)
    except asyncio.TimeoutError:
        print("Task took too long!")
```

## Concurrent Operations

### Gathering Tasks
```python
async def fetch_data(url):
    await asyncio.sleep(1)  # Simulate HTTP request
    return f"Data from {url}"

async def fetch_all():
    urls = [
        "http://example.com",
        "http://example.org",
        "http://example.net"
    ]
    
    tasks = [
        asyncio.create_task(fetch_data(url))
        for url in urls
    ]
    
    results = await asyncio.gather(*tasks)
    return results
```

### Race Conditions
```python
async def race_tasks():
    task1 = asyncio.create_task(
        fetch_data("http://fast.com"))
    task2 = asyncio.create_task(
        fetch_data("http://slow.com"))
    
    # Return result of first completed task
    done, pending = await asyncio.wait(
        [task1, task2],
        return_when=asyncio.FIRST_COMPLETED
    )
    
    # Cancel pending tasks
    for task in pending:
        task.cancel()
```

## Best Practices

### Proper Task Cleanup
```python
async def cleanup_tasks():
    try:
        task = asyncio.create_task(long_operation())
        await asyncio.shield(task)
    except asyncio.CancelledError:
        print("Operation cancelled")
        # Ensure task is properly cleaned up
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
```

### Resource Management
```python
class AsyncPool:
    def __init__(self, size):
        self.size = size
        self.semaphore = asyncio.Semaphore(size)
    
    async def acquire(self):
        await self.semaphore.acquire()
    
    async def release(self):
        self.semaphore.release()
    
    async def __aenter__(self):
        await self.acquire()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.release()

async def use_pool():
    pool = AsyncPool(3)
    async with pool:
        await some_operation()
```

## Common Patterns

### Producer-Consumer
```python
async def producer(queue):
    for i in range(5):
        await queue.put(i)
        await asyncio.sleep(1)
    await queue.put(None)  # End signal

async def consumer(queue):
    while True:
        item = await queue.get()
        if item is None:
            break
        print(f"Consumed {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    producer_task = asyncio.create_task(producer(queue))
    consumer_task = asyncio.create_task(consumer(queue))
    await asyncio.gather(producer_task, consumer_task)
```

### Event-Based Programming
```python
class AsyncEventEmitter:
    def __init__(self):
        self.events = {}
    
    def on(self, event, callback):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(callback)
    
    async def emit(self, event, *args, **kwargs):
        if event in self.events:
            for callback in self.events[event]:
                await callback(*args, **kwargs)

async def main():
    emitter = AsyncEventEmitter()
    
    async def handle_event(data):
        print(f"Received: {data}")
    
    emitter.on("data", handle_event)
    await emitter.emit("data", "Hello World")
```

## Exercises

1. Create an async web scraper that fetches multiple pages concurrently
2. Implement an async connection pool for database operations
3. Build an async rate limiter using semaphores
4. Create an async file processor that handles multiple files
5. Implement an async cache with timeout functionality