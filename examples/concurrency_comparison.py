"""
Comparison of different Python concurrency approaches:
- Threading (for I/O-bound tasks)
- Multiprocessing (for CPU-bound tasks)
- Asyncio (for I/O-bound tasks with many concurrent operations)
"""

import threading
import multiprocessing
import asyncio
import time
import requests
import aiohttp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from typing import List, Callable, Any

# Example I/O-bound task: Fetching URLs
URLS = [
    'https://api.github.com/events',
    'https://api.github.com/repos/python/cpython',
    'https://api.github.com/repos/pallets/flask',
] * 3  # Repeat URLs to have more tasks

def fetch_url(url: str) -> dict:
    """Fetch URL using requests (blocking I/O operation)"""
    response = requests.get(url)
    return response.json()

# Example CPU-bound task
def cpu_intensive(n: int) -> int:
    """Compute sum of squares (CPU-intensive operation)"""
    return sum(i * i for i in range(n))

# Threading example
def threading_example() -> None:
    """Demonstrate threading for I/O-bound tasks"""
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(fetch_url, URLS))
    
    duration = time.time() - start_time
    print(f"Threading took {duration:.2f} seconds")
    return results

# Multiprocessing example
def multiprocessing_example() -> None:
    """Demonstrate multiprocessing for CPU-bound tasks"""
    numbers = [10**6, 10**6, 10**6]  # Large numbers for CPU work
    start_time = time.time()
    
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(cpu_intensive, numbers))
    
    duration = time.time() - start_time
    print(f"Multiprocessing took {duration:.2f} seconds")
    return results

# Asyncio example
async def fetch_url_async(url: str, session: aiohttp.ClientSession) -> dict:
    """Fetch URL using aiohttp (non-blocking I/O operation)"""
    async with session.get(url) as response:
        return await response.json()

async def asyncio_example() -> List[dict]:
    """Demonstrate asyncio for I/O-bound tasks"""
    start_time = time.time()
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url_async(url, session)
            for url in URLS
        ]
        results = await asyncio.gather(*tasks)
    
    duration = time.time() - start_time
    print(f"Asyncio took {duration:.2f} seconds")
    return results

# Combined example showing a real-world scenario
class DataProcessor:
    def __init__(self, urls: List[str], numbers: List[int]):
        self.urls = urls
        self.numbers = numbers
        self.results: List[Any] = []
        self.queue = multiprocessing.Queue()
    
    def process_data(self) -> None:
        """Process both I/O-bound and CPU-bound tasks efficiently"""
        # Start CPU-intensive work in separate processes
        with ProcessPoolExecutor() as process_executor:
            cpu_futures = [
                process_executor.submit(cpu_intensive, n)
                for n in self.numbers
            ]
        
        # While CPU work is running, fetch URLs in threads
        with ThreadPoolExecutor() as thread_executor:
            io_futures = [
                thread_executor.submit(fetch_url, url)
                for url in self.urls
            ]
        
        # Collect all results
        for future in cpu_futures + io_futures:
            self.results.append(future.result())

def main() -> None:
    # Run examples
    print("Running concurrency examples...")
    
    # Threading for I/O-bound tasks
    thread_results = threading_example()
    
    # Multiprocessing for CPU-bound tasks
    process_results = multiprocessing_example()
    
    # Asyncio for I/O-bound tasks
    asyncio_results = asyncio.run(asyncio_example())
    
    # Combined real-world example
    processor = DataProcessor(
        urls=URLS[:3],  # Use fewer URLs for demonstration
        numbers=[10**6, 10**6, 10**6]
    )
    processor.process_data()

if __name__ == '__main__':
    main()