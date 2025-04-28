# Python Concurrency

## Threading Basics

### Thread Creation
```python
import threading
from typing import List, Callable
from time import sleep

def worker(name: str) -> None:
    """Basic thread worker function"""
    print(f"Worker {name} starting")
    sleep(2)
    print(f"Worker {name} finished")

# Creating and starting threads
thread1 = threading.Thread(target=worker, args=("1",))
thread2 = threading.Thread(target=worker, args=("2",))

thread1.start()
thread2.start()

# Wait for threads to complete
thread1.join()
thread2.join()
```

### Thread Pool
```python
from concurrent.futures import ThreadPoolExecutor
from typing import List

def process_item(item: int) -> int:
    """Example worker function"""
    return item * item

# Using thread pool
with ThreadPoolExecutor(max_workers=3) as executor:
    numbers = [1, 2, 3, 4, 5]
    results = list(executor.map(process_item, numbers))
```

## Multiprocessing

### Basic Process Creation
```python
from multiprocessing import Process, cpu_count
import os

def worker_process() -> None:
    """Worker function for process"""
    print(f"Worker process {os.getpid()} running")

if __name__ == '__main__':
    processes: List[Process] = []
    
    # Create multiple processes
    for _ in range(cpu_count()):
        p = Process(target=worker_process)
        processes.append(p)
        p.start()
    
    # Wait for all processes
    for p in processes:
        p.join()
```

### Process Pool
```python
from multiprocessing import Pool

def heavy_computation(n: int) -> int:
    """CPU-intensive task"""
    return sum(i * i for i in range(n))

if __name__ == '__main__':
    numbers = [1000000, 2000000, 3000000]
    
    # Using process pool
    with Pool() as pool:
        results = pool.map(heavy_computation, numbers)
```

## Asynchronous Programming

### Basic Coroutines
```python
import asyncio
from typing import List

async def async_task(name: str, delay: float) -> None:
    """Simple coroutine"""
    print(f"Task {name} starting")
    await asyncio.sleep(delay)
    print(f"Task {name} completed")

async def main() -> None:
    # Create tasks
    tasks = [
        async_task("A", 2),
        async_task("B", 1),
        async_task("C", 3)
    ]
    
    # Run tasks concurrently
    await asyncio.gather(*tasks)

# Run the async program
asyncio.run(main())
```

### Async Context Managers
```python
from typing import AsyncIterator
import aiohttp
import asyncio

class AsyncResource:
    async def __aenter__(self) -> 'AsyncResource':
        print("Acquiring resource")
        await asyncio.sleep(1)  # Simulate resource acquisition
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        print("Releasing resource")
        await asyncio.sleep(1)  # Simulate resource release

async def use_resource() -> None:
    async with AsyncResource() as resource:
        print("Using resource")
```

## Synchronization

### Locks and Semaphores
```python
import threading
from typing import List

class SharedCounter:
    def __init__(self) -> None:
        self.count = 0
        self.lock = threading.Lock()
    
    def increment(self) -> None:
        with self.lock:
            self.count += 1

# Using Semaphore
semaphore = threading.Semaphore(2)  # Allow 2 concurrent accesses

def limited_resource() -> None:
    with semaphore:
        print("Accessing limited resource")
        sleep(2)
```

### Event and Condition
```python
class DataQueue:
    def __init__(self, max_size: int) -> None:
        self.queue: List[str] = []
        self.max_size = max_size
        self.condition = threading.Condition()
    
    def put(self, item: str) -> None:
        with self.condition:
            while len(self.queue) >= self.max_size:
                self.condition.wait()
            self.queue.append(item)
            self.condition.notify()
    
    def get(self) -> str:
        with self.condition:
            while not self.queue:
                self.condition.wait()
            item = self.queue.pop(0)
            self.condition.notify()
            return item
```

## Best Practices

### Thread vs Process Selection
```python
# CPU-bound tasks: Use multiprocessing
def cpu_intensive() -> None:
    with Pool() as pool:
        results = pool.map(heavy_computation, data)

# I/O-bound tasks: Use threading or asyncio
def io_intensive() -> None:
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(fetch_url, url) 
                  for url in urls]
```

### Resource Management
```python
from contextlib import contextmanager
from typing import Iterator

@contextmanager
def managed_resource() -> Iterator[None]:
    """Thread-safe resource management"""
    try:
        print("Acquiring resource")
        yield
    finally:
        print("Releasing resource")

def use_resource() -> None:
    with managed_resource():
        print("Using resource safely")
```

## Common Patterns

### Producer-Consumer
```python
from queue import Queue
from threading import Thread
from typing import Optional

class ProducerConsumer:
    def __init__(self) -> None:
        self.queue: Queue = Queue(maxsize=10)
    
    def producer(self) -> None:
        for i in range(20):
            self.queue.put(f"Item {i}")
    
    def consumer(self) -> None:
        while True:
            item: Optional[str] = self.queue.get()
            if item is None:
                break
            print(f"Processed {item}")
            self.queue.task_done()

    def run(self) -> None:
        # Start producer and consumer threads
        producer = Thread(target=self.producer)
        consumer = Thread(target=self.consumer)
        
        producer.start()
        consumer.start()
        
        producer.join()
        self.queue.put(None)  # Signal to stop consumer
        consumer.join()
```

### Task Pool Pattern
```python
import asyncio
from typing import List, Callable, Awaitable, TypeVar

T = TypeVar('T')

class AsyncTaskPool:
    def __init__(self, max_workers: int) -> None:
        self.semaphore = asyncio.Semaphore(max_workers)
        self.tasks: List[asyncio.Task] = []
    
    async def add_task(self, coro: Awaitable[T]) -> None:
        async with self.semaphore:
            task = asyncio.create_task(coro)
            self.tasks.append(task)
            await task
    
    async def join(self) -> None:
        if self.tasks:
            await asyncio.gather(*self.tasks)
```

# Concurrent Functional Programming in Python

## Core Patterns

### Async Pipeline Pattern
```python
from typing import Awaitable, List
from dataclasses import dataclass

# Type-safe async pipeline
pipeline = AsyncPipeline([
    lambda x: asyncio.sleep(0.1, result=x * 2),
    lambda x: asyncio.sleep(0.1, result=str(x))
])
result = await pipeline.process(5)
```

### Parallel Map Pattern
```python
# Process data in parallel chunks
processor = DataProcessor(chunk_size=1000)
results = processor.parallel_process(data, expensive_function)

# Async parallel processing
results = await processor.parallel_map.async_map(async_function, items)
```

### Monadic Error Handling
```python
# AsyncResult monad for error handling
result = await AsyncResult.success(10).map(async_double)
if isinstance(result, AsyncSuccess):
    value = await result.run()
else:
    error = result.get_error()
```

## Common Patterns

### Rate Limiting
```python
# Rate-limited async pipeline
pipeline = RateLimitedPipeline(
    steps=[async_process],
    rate_limit=10  # requests per second
)
result = await pipeline.process(data)
```

### Concurrent HTTP Client
```python
# Retry and backoff
client = AsyncHTTPClient(max_retries=3, backoff_factor=1.0)
result = await client.fetch("https://api.example.com")

# Parallel requests with rate limiting
results = await client.fetch_all([
    "https://api.example.com/1",
    "https://api.example.com/2"
])
```

## Best Practices

1. Error Handling
   - Use monadic error handling (AsyncResult)
   - Implement proper retry mechanisms
   - Handle timeouts and backoff

2. Resource Management
   - Use context managers for resources
   - Implement proper cleanup
   - Monitor resource usage

3. Performance
   - Choose appropriate chunk sizes
   - Balance parallelism and resource usage
   - Use profiling to optimize

4. Rate Limiting
   - Implement token bucket algorithm
   - Use sliding window rate limiting
   - Handle bursts appropriately

## Common Pitfalls

1. Resource Exhaustion
   ```python
   # BAD: Unlimited concurrent tasks
   tasks = [async_function() for _ in range(1000)]
   await asyncio.gather(*tasks)
   
   # GOOD: Limited concurrency
   semaphore = asyncio.Semaphore(10)
   async with semaphore:
       await async_function()
   ```

2. Error Propagation
   ```python
   # BAD: Swallowing errors
   try:
       await async_function()
   except Exception:
       pass
   
   # GOOD: Proper error handling
   result = await AsyncResult.success(data).map(async_function)
   if not result.is_success():
       handle_error(result.get_error())
   ```

3. Memory Management
   ```python
   # BAD: Loading all data at once
   data = list(generate_large_dataset())
   results = process_parallel(data)
   
   # GOOD: Chunked processing
   processor = DataProcessor(chunk_size=1000)
   for chunk in processor.chunk_data(generate_large_dataset()):
       results = await process_chunk(chunk)
   ```

## Advanced Patterns

### Parallel Pipeline
```python
class ParallelPipeline:
    def __init__(self, max_workers: int):
        self.executor = ProcessPoolExecutor(max_workers)
        
    async def process(self, items: List[T]) -> List[U]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self.parallel_process,
            items
        )
```

### Reactive Patterns
```python
from typing import AsyncIterator

async def reactive_pipeline(source: AsyncIterator[T]) -> AsyncIterator[U]:
    async for item in source:
        yield await transform(item)

# Usage
async for result in reactive_pipeline(data_source):
    process_result(result)
```

### Backpressure Handling
```python
class BackpressureQueue:
    def __init__(self, maxsize: int):
        self.queue = asyncio.Queue(maxsize)
    
    async def produce(self, item: T):
        await self.queue.put(item)  # Blocks when full
    
    async def consume() -> T:
        return await self.queue.get()  # Blocks when empty
```

## Testing Patterns

1. Mocking Async Code
   ```python
   @pytest.mark.asyncio
   async def test_async_function(mocker):
       mock = mocker.AsyncMock(return_value=42)
       result = await async_function(mock)
       assert result == 42
   ```

2. Testing Rate Limiting
   ```python
   @pytest.mark.asyncio
   async def test_rate_limiter():
       limiter = RateLimiter(rate_limit=2)
       start = time.monotonic()
       await limiter.acquire()
       await limiter.acquire()
       await limiter.acquire()  # Should wait
       assert time.monotonic() - start >= 0.5
   ```

3. Integration Testing
   ```python
   @pytest.mark.asyncio
   async def test_pipeline_integration():
       pipeline = AsyncPipeline([
           fetch_data,
           process_data,
           store_results
       ])
       result = await pipeline.process(test_data)
       assert validate_result(result)
   ```

## Performance Optimization

1. Profile Async Code
   ```python
   import asyncio
   import cProfile
   
   async def main():
       profiler = cProfile.Profile()
       profiler.enable()
       try:
           await async_function()
       finally:
           profiler.disable()
           profiler.print_stats(sort='cumtime')
   ```

2. Memory Optimization
   ```python
   from memory_profiler import profile
   
   @profile
   def process_large_data():
       processor = DataProcessor(chunk_size=optimal_chunk_size())
       for chunk in processor.chunk_data(data_source()):
           process_chunk(chunk)
   ```

3. Concurrency Tuning
   ```python
   import multiprocessing
   
   def optimal_workers():
       return min(32, multiprocessing.cpu_count() * 2)
   
   processor = ParallelMap(max_workers=optimal_workers())
   ```