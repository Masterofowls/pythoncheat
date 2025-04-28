"""
Implementation of concurrent functional programming patterns in Python.
Provides reusable components for building concurrent functional pipelines.
"""
from __future__ import annotations
import asyncio
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from typing import (
    TypeVar, Generic, List, Callable, Awaitable, Optional,
    Any, Dict, AsyncIterator, Iterator
)
import aiohttp
from functools import wraps

T = TypeVar('T')
U = TypeVar('U')

class AsyncPipeline(Generic[T, U]):
    """A pipeline that processes data through a series of async functions"""
    def __init__(self, steps: List[Callable[[Any], Awaitable[Any]]]):
        self.steps = steps
    
    async def process(self, input_data: T) -> U:
        """Process input through all pipeline steps"""
        result = input_data
        for step in self.steps:
            result = await step(result)
        return result
    
    def add_step(self, step: Callable[[Any], Awaitable[Any]]) -> AsyncPipeline:
        """Add a new step to the pipeline, returns new pipeline"""
        return AsyncPipeline(self.steps + [step])

class ParallelMap:
    """Execute operations in parallel using process pool"""
    def __init__(self, max_workers: Optional[int] = None):
        self.max_workers = max_workers or min(32, ProcessPoolExecutor()._max_workers)
    
    def map(self, func: Callable[[T], U], items: List[T]) -> List[U]:
        """Map function over items in parallel"""
        with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(func, items))
    
    async def async_map(self, func: Callable[[T], Awaitable[U]], 
                       items: List[T]) -> List[U]:
        """Map async function over items in parallel"""
        tasks = [func(item) for item in items]
        return await asyncio.gather(*tasks)

@dataclass
class AsyncSuccess(Generic[T]):
    """Represents successful async computation"""
    value: T
    
    async def run(self) -> T:
        return self.value
    
    async def map(self, func: Callable[[T], Awaitable[U]]) -> AsyncResult[U]:
        try:
            result = await func(self.value)
            return AsyncSuccess(result)
        except Exception as e:
            return AsyncFailure(e)
    
    def is_success(self) -> bool:
        return True

@dataclass
class AsyncFailure(Generic[T]):
    """Represents failed async computation"""
    error: Exception
    
    async def run(self) -> T:
        raise self.error
    
    async def map(self, func: Callable[[T], Awaitable[U]]) -> AsyncResult[U]:
        return AsyncFailure(self.error)
    
    def is_success(self) -> bool:
        return False
    
    def get_error(self) -> Exception:
        return self.error

AsyncResult = AsyncSuccess[T] | AsyncFailure[T]

class AsyncHTTPClient:
    """HTTP client with retry and rate limiting"""
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None:
            self._session = aiohttp.ClientSession()
        return self._session
    
    async def fetch(self, url: str) -> AsyncResult[Dict[str, Any]]:
        """Fetch URL with retry logic"""
        session = await self._get_session()
        for attempt in range(self.max_retries):
            try:
                async with session.get(url) as response:
                    data = await response.json()
                    return AsyncSuccess(data)
            except Exception as e:
                if attempt == self.max_retries - 1:
                    return AsyncFailure(e)
                await asyncio.sleep(self.backoff_factor * (2 ** attempt))
    
    async def fetch_all(self, urls: List[str]) -> List[AsyncResult[Dict[str, Any]]]:
        """Fetch multiple URLs in parallel"""
        return await asyncio.gather(*(self.fetch(url) for url in urls))
    
    async def close(self) -> None:
        """Close the session"""
        if self._session:
            await self._session.close()
            self._session = None

class DataProcessor(Generic[T, U]):
    """Process data in chunks with parallel execution"""
    def __init__(self, chunk_size: int = 1000):
        self.chunk_size = chunk_size
    
    def chunk_data(self, data: List[T]) -> Iterator[List[T]]:
        """Split data into chunks"""
        for i in range(0, len(data), self.chunk_size):
            yield data[i:i + self.chunk_size]
    
    def parallel_process(self, data: List[T], 
                        func: Callable[[T], U]) -> List[U]:
        """Process data in parallel chunks"""
        mapper = ParallelMap()
        chunks = list(self.chunk_data(data))
        results = []
        
        for chunk in chunks:
            chunk_results = mapper.map(func, chunk)
            results.extend(chunk_results)
        
        return results

class RateLimiter:
    """Token bucket rate limiter"""
    def __init__(self, rate_limit: float, time_window: float = 1.0):
        self.rate_limit = rate_limit
        self.time_window = time_window
        self.tokens = rate_limit
        self.last_update = time.monotonic()
        self._lock = asyncio.Lock()
    
    async def acquire(self) -> None:
        """Acquire a token, waiting if necessary"""
        async with self._lock:
            while self.tokens <= 0:
                now = time.monotonic()
                time_passed = now - self.last_update
                self.tokens = min(
                    self.rate_limit,
                    self.tokens + time_passed * (self.rate_limit / self.time_window)
                )
                self.last_update = now
                if self.tokens <= 0:
                    await asyncio.sleep(self.time_window / self.rate_limit)
            
            self.tokens -= 1

class RateLimitedPipeline(AsyncPipeline[T, U]):
    """Pipeline with rate limiting"""
    def __init__(self, steps: List[Callable[[Any], Awaitable[Any]]], 
                 rate_limit: float = 10.0):
        super().__init__(steps)
        self.rate_limiter = RateLimiter(rate_limit)
    
    async def process(self, input_data: T) -> U:
        """Process with rate limiting"""
        await self.rate_limiter.acquire()
        return await super().process(input_data)

async def with_backpressure(source: AsyncIterator[T], 
                           max_buffer: int = 100) -> AsyncIterator[T]:
    """Add backpressure to an async iterator"""
    queue = asyncio.Queue(maxsize=max_buffer)
    
    async def producer():
        async for item in source:
            await queue.put(item)
        await queue.put(None)  # Signal end
    
    producer_task = asyncio.create_task(producer())
    
    try:
        while True:
            item = await queue.get()
            if item is None:
                break
            yield item
    finally:
        producer_task.cancel()
        try:
            await producer_task
        except asyncio.CancelledError:
            pass

def profile_async(func: Callable[..., Awaitable[T]]) -> Callable[..., Awaitable[T]]:
    """Profile an async function"""
    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> T:
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()
        try:
            return await func(*args, **kwargs)
        finally:
            profiler.disable()
            stats = pstats.Stats(profiler)
            stats.sort_stats('cumtime')
            stats.print_stats()
    return wrapper