"""
Real-world examples of Python optimization patterns.
This module demonstrates practical applications of optimization techniques.
"""
import time
import cProfile
import asyncio
import aiohttp
from typing import List, Dict, Set, Generator, Any
from dataclasses import dataclass
from functools import lru_cache
from concurrent.futures import ProcessPoolExecutor
import json
import sys
from pathlib import Path

@dataclass
class DataPoint:
    """Example data structure for optimization demos"""
    id: int
    value: float
    metadata: Dict[str, Any]

class DataProcessor:
    """Demonstrates different approaches to data processing"""
    
    def __init__(self, cache_size: int = 1000):
        self.cache_size = cache_size
        self._cache: Dict[int, DataPoint] = {}
    
    def process_data_simple(self, data_points: List[DataPoint]) -> Dict[int, float]:
        """Unoptimized data processing"""
        result = {}
        for point in data_points:
            # Inefficient: Recalculates for same IDs
            result[point.id] = self._expensive_calculation(point.value)
        return result
    
    def process_data_optimized(self, data_points: List[DataPoint]) -> Dict[int, float]:
        """Optimized data processing with caching"""
        result = {}
        for point in data_points:
            if point.id in self._cache:
                result[point.id] = self._cache[point.id].value
            else:
                result[point.id] = self._expensive_calculation(point.value)
                # Implement LRU-like behavior
                if len(self._cache) >= self.cache_size:
                    self._cache.pop(next(iter(self._cache)))
                self._cache[point.id] = point
        return result
    
    @staticmethod
    def _expensive_calculation(value: float) -> float:
        """Simulate an expensive calculation"""
        time.sleep(0.1)  # Simulate work
        return value ** 2

class FileProcessor:
    """Demonstrates memory-efficient file processing"""
    
    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size
    
    def process_file_simple(self, filepath: Path) -> List[str]:
        """Memory-intensive file processing"""
        with open(filepath, 'r') as f:
            return [line.strip() for line in f.readlines()]
    
    def process_file_generator(self, filepath: Path) -> Generator[str, None, None]:
        """Memory-efficient file processing"""
        with open(filepath, 'r') as f:
            for line in f:
                yield line.strip()
    
    async def process_files_async(self, filepaths: List[Path]) -> List[str]:
        """Concurrent file processing"""
        async def read_file(path: Path) -> str:
            with open(path, 'r') as f:
                return f.read()
        
        tasks = [read_file(path) for path in filepaths]
        return await asyncio.gather(*tasks)

class ParallelProcessor:
    """Demonstrates parallel processing optimizations"""
    
    @staticmethod
    def process_data_serial(items: List[int]) -> List[int]:
        """Serial processing"""
        return [ParallelProcessor._cpu_intensive_task(item) for item in items]
    
    @staticmethod
    def process_data_parallel(items: List[int], workers: int = None) -> List[int]:
        """Parallel processing"""
        with ProcessPoolExecutor(max_workers=workers) as executor:
            return list(executor.map(
                ParallelProcessor._cpu_intensive_task, 
                items
            ))
    
    @staticmethod
    def _cpu_intensive_task(n: int) -> int:
        """Simulate CPU-intensive computation"""
        return sum(i * i for i in range(n))

class APIClient:
    """Demonstrates I/O optimization patterns"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self._cache: Dict[str, Any] = {}
    
    def fetch_data_simple(self, endpoints: List[str]) -> List[Dict]:
        """Sequential API calls"""
        import requests
        results = []
        for endpoint in endpoints:
            url = f"{self.base_url}/{endpoint}"
            if url in self._cache:
                results.append(self._cache[url])
            else:
                response = requests.get(url)
                data = response.json()
                self._cache[url] = data
                results.append(data)
        return results
    
    async def fetch_data_concurrent(self, endpoints: List[str]) -> List[Dict]:
        """Concurrent API calls"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for endpoint in endpoints:
                url = f"{self.base_url}/{endpoint}"
                if url in self._cache:
                    tasks.append(asyncio.create_task(
                        asyncio.sleep(0, result=self._cache[url])
                    ))
                else:
                    tasks.append(self.fetch_endpoint(session, endpoint))
            return await asyncio.gather(*tasks)
    
    async def fetch_endpoint(self, 
                           session: aiohttp.ClientSession, 
                           endpoint: str) -> Dict:
        """Fetch single endpoint with caching"""
        url = f"{self.base_url}/{endpoint}"
        async with session.get(url) as response:
            data = await response.json()
            self._cache[url] = data
            return data

def demonstrate_optimizations():
    """Run optimization demonstrations"""
    # Data processing optimization
    data_points = [
        DataPoint(i, float(i), {"meta": f"data_{i}"})
        for i in range(100)
    ]
    
    processor = DataProcessor()
    
    print("Running unoptimized processing...")
    start = time.time()
    processor.process_data_simple(data_points[:10])
    print(f"Unoptimized time: {time.time() - start:.2f}s")
    
    print("\nRunning optimized processing...")
    start = time.time()
    processor.process_data_optimized(data_points[:10])
    print(f"Optimized time: {time.time() - start:.2f}s")
    
    # Parallel processing
    items = [1000000 + i for i in range(10)]
    parallel = ParallelProcessor()
    
    print("\nRunning serial processing...")
    start = time.time()
    parallel.process_data_serial(items[:4])
    print(f"Serial time: {time.time() - start:.2f}s")
    
    print("\nRunning parallel processing...")
    start = time.time()
    parallel.process_data_parallel(items[:4])
    print(f"Parallel time: {time.time() - start:.2f}s")

if __name__ == '__main__':
    demonstrate_optimizations()
    
    # Profile the demonstration
    print("\nProfiling demonstration...")
    cProfile.run('demonstrate_optimizations()', sort='cumulative')