# Python Concurrency Patterns

## Threading

### Basic Threading
```python
import threading
from typing import List, Callable, Any
from queue import Queue
from concurrent.futures import ThreadPoolExecutor

def worker(queue: Queue) -> None:
    while True:
        item = queue.get()
        if item is None:
            break
        process_item(item)
        queue.task_done()

# Create and start threads
queue = Queue()
threads: List[threading.Thread] = []
for _ in range(3):
    t = threading.Thread(target=worker, args=(queue,))
    t.start()
    threads.append(t)

# Add work to the queue
for item in items:
    queue.put(item)

# Add None to signal threads to exit
for _ in threads:
    queue.put(None)

# Wait for all threads to complete
for t in threads:
    t.join()
```

### Thread Pool
```python
def process_url(url: str) -> str:
    # Simulate web request
    time.sleep(0.1)
    return f"Processed {url}"

urls = [f"http://example.com/{i}" for i in range(10)]

with ThreadPoolExecutor(max_workers=3) as executor:
    # Map version
    results = list(executor.map(process_url, urls))
    
    # Submit version
    future_to_url = {
        executor.submit(process_url, url): url
        for url in urls
    }
    
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            result = future.result()
        except Exception as e:
            print(f"{url} generated an exception: {e}")
```

### Thread Safety
```python
from threading import Lock
from contextlib import contextmanager
from typing import Iterator

class ThreadSafeCounter:
    def __init__(self):
        self._count = 0
        self._lock = Lock()
    
    @contextmanager
    def get_lock(self) -> Iterator[None]:
        """Context manager for lock"""
        self._lock.acquire()
        try:
            yield
        finally:
            self._lock.release()
    
    def increment(self) -> None:
        with self._lock:
            self._count += 1
    
    def get_count(self) -> int:
        with self._lock:
            return self._count
```

## Multiprocessing

### Process Pool
```python
from multiprocessing import Pool
import math
from typing import List

def cpu_bound_task(n: int) -> int:
    """CPU-intensive calculation"""
    return sum(i * i for i in range(n))

def parallel_processing(numbers: List[int]) -> List[int]:
    # Number of CPU cores
    cpu_count = multiprocessing.cpu_count()
    
    # Create a pool of processes
    with Pool(processes=cpu_count) as pool:
        # Map the function to the inputs
        results = pool.map(cpu_bound_task, numbers)
    
    return results
```

### Process Communication
```python
from multiprocessing import Process, Pipe
from multiprocessing.connection import Connection
from typing import Tuple

def worker(conn: Connection) -> None:
    """Worker process function"""
    while True:
        msg = conn.recv()
        if msg == "STOP":
            break
        # Process the message
        result = process_message(msg)
        conn.send(result)

def main() -> None:
    # Create pipe
    parent_conn, child_conn = Pipe()
    
    # Create and start process
    p = Process(target=worker, args=(child_conn,))
    p.start()
    
    # Send work
    for item in work_items:
        parent_conn.send(item)
        result = parent_conn.recv()
        print(f"Got result: {result}")
    
    # Signal process to stop
    parent_conn.send("STOP")
    p.join()
```

### Shared Memory
```python
from multiprocessing import shared_memory
import numpy as np
from typing import Optional

class SharedArray:
    def __init__(
        self,
        name: str,
        shape: Tuple[int, ...],
        dtype: np.dtype
    ):
        self.shape = shape
        self.dtype = dtype
        
        try:
            # Try to attach to existing shared memory
            self.shm = shared_memory.SharedMemory(name=name)
            self.array = np.ndarray(
                shape,
                dtype=dtype,
                buffer=self.shm.buf
            )
        except FileNotFoundError:
            # Create new shared memory
            temp_array = np.zeros(shape, dtype=dtype)
            self.shm = shared_memory.SharedMemory(
                name=name,
                create=True,
                size=temp_array.nbytes
            )
            self.array = np.ndarray(
                shape,
                dtype=dtype,
                buffer=self.shm.buf
            )
    
    def close(self) -> None:
        """Close the shared memory block"""
        self.shm.close()
    
    def unlink(self) -> None:
        """Remove the shared memory block"""
        self.shm.unlink()
```

## Asyncio

### Basic Coroutines
```python
import asyncio
from typing import List

async def fetch_data(url: str) -> str:
    """Simulate async HTTP request"""
    await asyncio.sleep(1)  # Simulate network delay
    return f"Data from {url}"

async def process_urls(urls: List[str]) -> List[str]:
    """Process multiple URLs concurrently"""
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    return results

async def main() -> None:
    urls = [f"http://example.com/{i}" for i in range(5)]
    results = await process_urls(urls)
    print(results)

# Run the async program
asyncio.run(main())
```

### Async Context Managers
```python
from typing import AsyncIterator
import aiohttp
from contextlib import asynccontextmanager

@asynccontextmanager
async def http_session() -> AsyncIterator[aiohttp.ClientSession]:
    """Async context manager for HTTP sessions"""
    session = aiohttp.ClientSession()
    try:
        yield session
    finally:
        await session.close()

async def fetch_urls(urls: List[str]) -> List[str]:
    async with http_session() as session:
        tasks = []
        for url in urls:
            tasks.append(fetch_page(session, url))
        return await asyncio.gather(*tasks)

async def fetch_page(
    session: aiohttp.ClientSession,
    url: str
) -> str:
    async with session.get(url) as response:
        return await response.text()
```

### Async Queues
```python
import asyncio
from asyncio import Queue
from typing import List, Optional

async def producer(
    queue: Queue,
    items: List[str]
) -> None:
    """Produce items to the queue"""
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0.1)  # Simulate production time

async def consumer(
    queue: Queue,
    name: str
) -> None:
    """Consume items from the queue"""
    while True:
        item = await queue.get()
        if item is None:
            queue.task_done()
            break
        
        # Process the item
        await process_item(item)
        queue.task_done()

async def main() -> None:
    queue: Queue = Queue()
    items = [f"item_{i}" for i in range(10)]
    
    # Create producer and consumers
    producer_task = asyncio.create_task(
        producer(queue, items)
    )
    consumers = [
        asyncio.create_task(consumer(queue, f"consumer_{i}"))
        for i in range(3)
    ]
    
    # Wait for producer to finish
    await producer_task
    
    # Send stop signal to consumers
    for _ in consumers:
        await queue.put(None)
    
    # Wait for consumers to finish
    await asyncio.gather(*consumers)
```

## Advanced Patterns

### Event-Driven Architecture
```python
from typing import Dict, Set, Callable, Any
from collections import defaultdict

class EventEmitter:
    def __init__(self):
        self._events: Dict[str, Set[Callable]] = defaultdict(set)
    
    def on(self, event: str, handler: Callable) -> None:
        """Register an event handler"""
        self._events[event].add(handler)
    
    def off(self, event: str, handler: Callable) -> None:
        """Remove an event handler"""
        if event in self._events:
            self._events[event].discard(handler)
    
    async def emit(self, event: str, *args: Any) -> None:
        """Emit an event"""
        if event in self._events:
            for handler in self._events[event]:
                await handler(*args)

# Usage
async def main():
    emitter = EventEmitter()
    
    async def handle_data(data: str) -> None:
        print(f"Received: {data}")
    
    emitter.on("data", handle_data)
    await emitter.emit("data", "Hello, World!")
```

### Concurrent Pipeline
```python
import asyncio
from typing import AsyncIterator, TypeVar, Callable, Any

T = TypeVar('T')
U = TypeVar('U')

async def pipeline_stage(
    input_queue: Queue[T],
    output_queue: Queue[U],
    processor: Callable[[T], U]
) -> None:
    """A stage in the pipeline"""
    while True:
        item = await input_queue.get()
        if item is None:
            await output_queue.put(None)
            break
        result = await processor(item)
        await output_queue.put(result)

async def pipeline(
    source: AsyncIterator[T],
    *stages: Callable[[T], Any]
) -> AsyncIterator:
    """Create a processing pipeline"""
    queues = [Queue() for _ in range(len(stages) + 1)]
    
    # Start pipeline stages
    tasks = []
    for i, stage in enumerate(stages):
        task = asyncio.create_task(
            pipeline_stage(queues[i], queues[i + 1], stage)
        )
        tasks.append(task)
    
    # Feed data into pipeline
    async for item in source:
        await queues[0].put(item)
    
    # Signal end of data
    await queues[0].put(None)
    
    # Wait for all stages to complete
    await asyncio.gather(*tasks)
    
    # Yield results
    while True:
        result = await queues[-1].get()
        if result is None:
            break
        yield result
```

## Best Practices

### Resource Management
```python
from contextlib import asynccontextmanager
from typing import AsyncIterator, Any

class Resource:
    async def initialize(self) -> None:
        # Initialize the resource
        pass
    
    async def cleanup(self) -> None:
        # Clean up the resource
        pass
    
    async def use(self) -> Any:
        # Use the resource
        pass

@asynccontextmanager
async def managed_resource() -> AsyncIterator[Resource]:
    """Context manager for async resource"""
    resource = Resource()
    try:
        await resource.initialize()
        yield resource
    finally:
        await resource.cleanup()

async def main() -> None:
    async with managed_resource() as resource:
        result = await resource.use()
        print(result)
```

### Error Handling
```python
from typing import Optional, Callable, Any
import functools

def retry_async(
    retries: int = 3,
    delay: float = 1.0
) -> Callable:
    """Decorator for retrying async operations"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_error: Optional[Exception] = None
            
            for attempt in range(retries):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < retries - 1:
                        await asyncio.sleep(delay)
            
            raise last_error
        
        return wrapper
    return decorator

@retry_async(retries=3, delay=1.0)
async def fetch_with_retry(url: str) -> str:
    """Fetch URL with retry logic"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()
```

## Exercises

1. Implement a thread-safe cache
2. Create a process pool for image processing
3. Build an async web crawler
4. Implement a concurrent pipeline for data processing
5. Create a distributed task queue with Redis