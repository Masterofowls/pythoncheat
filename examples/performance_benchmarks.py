"""
Performance benchmarks for modern Python features.
Compares different implementations and approaches using the benchmarking utilities.
"""
from typing import List, Dict, Any, TypeVar, Generic
from dataclasses import dataclass
from datetime import datetime
import json
import time
from examples.benchmark_utils import (
    PerformanceBenchmark,
    benchmark
)

T = TypeVar('T')

# Different cache implementations for comparison
class DictCache(Generic[T]):
    """Simple dictionary-based cache"""
    def __init__(self):
        self._data: Dict[str, T] = {}
    
    def get(self, key: str) -> T:
        return self._data.get(key)
    
    def set(self, key: str, value: T) -> None:
        self._data[key] = value

class TimedDictCache(Generic[T]):
    """Dictionary cache with timestamp checking"""
    def __init__(self, timeout: int = 3600):
        self._data: Dict[str, tuple[T, float]] = {}
        self.timeout = timeout
    
    def get(self, key: str) -> T:
        if key in self._data:
            value, timestamp = self._data[key]
            if time.time() - timestamp < self.timeout:
                return value
            del self._data[key]
        return None
    
    def set(self, key: str, value: T) -> None:
        self._data[key] = (value, time.time())

class LRUCache(Generic[T]):
    """LRU cache implementation"""
    def __init__(self, capacity: int = 100):
        self._data: Dict[str, T] = {}
        self._usage: List[str] = []
        self.capacity = capacity
    
    def get(self, key: str) -> T:
        if key in self._data:
            self._usage.remove(key)
            self._usage.append(key)
            return self._data[key]
        return None
    
    def set(self, key: str, value: T) -> None:
        if key in self._data:
            self._usage.remove(key)
        elif len(self._data) >= self.capacity:
            oldest = self._usage.pop(0)
            del self._data[oldest]
        
        self._data[key] = value
        self._usage.append(key)

# Test data for benchmarking
@dataclass
class TestData:
    id: int
    name: str
    data: Dict[str, Any]

def generate_test_data(size: int) -> List[TestData]:
    """Generate test data for benchmarks"""
    return [
        TestData(
            id=i,
            name=f"item_{i}",
            data={
                "value": i * 100,
                "timestamp": datetime.now().isoformat(),
                "metadata": {"tag": f"tag_{i}"}
            }
        )
        for i in range(size)
    ]

# Benchmark different cache implementations
def benchmark_caches() -> None:
    """Compare performance of different cache implementations"""
    benchmark = PerformanceBenchmark(iterations=5)
    test_data = generate_test_data(1000)
    
    def test_dict_cache() -> None:
        cache = DictCache[TestData]()
        for item in test_data:
            cache.set(str(item.id), item)
        for i in range(len(test_data)):
            _ = cache.get(str(i))
    
    def test_timed_cache() -> None:
        cache = TimedDictCache[TestData](timeout=3600)
        for item in test_data:
            cache.set(str(item.id), item)
        for i in range(len(test_data)):
            _ = cache.get(str(i))
    
    def test_lru_cache() -> None:
        cache = LRUCache[TestData](capacity=1000)
        for item in test_data:
            cache.set(str(item.id), item)
        for i in range(len(test_data)):
            _ = cache.get(str(i))
    
    # Run benchmarks
    benchmark.compare_implementations({
        "dict_cache": test_dict_cache,
        "timed_cache": test_timed_cache,
        "lru_cache": test_lru_cache
    })
    
    # Generate plots
    benchmark.plot_results()

# Benchmark different serialization approaches
def benchmark_serialization() -> None:
    """Compare performance of different serialization approaches"""
    benchmark = PerformanceBenchmark(iterations=5)
    test_data = generate_test_data(1000)
    
    def test_json_dumps() -> None:
        for item in test_data:
            _ = json.dumps({
                "id": item.id,
                "name": item.name,
                "data": item.data
            })
    
    def test_manual_dict() -> None:
        for item in test_data:
            _ = str({
                "id": item.id,
                "name": item.name,
                "data": item.data
            })
    
    def test_dataclass_dict() -> None:
        for item in test_data:
            _ = str({
                field: getattr(item, field)
                for field in ["id", "name", "data"]
            })
    
    # Run benchmarks
    benchmark.compare_implementations({
        "json_dumps": test_json_dumps,
        "manual_dict": test_manual_dict,
        "dataclass_dict": test_dataclass_dict
    })
    
    # Generate plots
    benchmark.plot_results()

# Benchmark different string operations
def benchmark_string_operations() -> None:
    """Compare performance of different string operation approaches"""
    benchmark = PerformanceBenchmark(iterations=5)
    test_strings = ["test_string" * 100 for _ in range(1000)]
    
    def test_plus_concat() -> None:
        result = ""
        for s in test_strings:
            result = result + s
    
    def test_join() -> None:
        result = "".join(test_strings)
    
    def test_fstring() -> None:
        result = ""
        for s in test_strings:
            result = f"{result}{s}"
    
    # Run benchmarks
    benchmark.compare_implementations({
        "plus_concat": test_plus_concat,
        "join": test_join,
        "fstring": test_fstring
    })
    
    # Generate plots
    benchmark.plot_results()

def demonstrate_benchmarks() -> None:
    """Run all benchmarks and display results"""
    print("\nRunning cache implementation benchmarks...")
    benchmark_caches()
    
    print("\nRunning serialization benchmarks...")
    benchmark_serialization()
    
    print("\nRunning string operation benchmarks...")
    benchmark_string_operations()

if __name__ == '__main__':
    demonstrate_benchmarks()