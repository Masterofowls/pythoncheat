# Algorithm Optimization in Python

## Memory Optimization Patterns

### Generator-based Iteration
```python
# Instead of loading entire dataset into memory
def process_large_file(filename: str) -> List[str]:
    with open(filename) as f:
        return [line.strip() for line in f]  # Memory intensive

# Use generator to process line by line
def process_large_file(filename: str) -> Iterator[str]:
    with open(filename) as f:
        for line in f:
            yield line.strip()  # Memory efficient
```

### Memoization Strategies
```python
from functools import lru_cache
from typing import Dict, TypeVar, Callable, Any

# Simple dict-based memoization
def memoize(func: Callable) -> Callable:
    cache: Dict = {}
    def wrapper(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return wrapper

# LRU Cache with size limit
@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Timed cache for dynamic data
from time import time
def timed_cache(timeout: int):
    def decorator(func: Callable) -> Callable:
        cache: Dict[str, Tuple[float, Any]] = {}
        def wrapper(*args, **kwargs):
            key = str(args) + str(kwargs)
            if key in cache:
                timestamp, value = cache[key]
                if time() - timestamp < timeout:
                    return value
            result = func(*args, **kwargs)
            cache[key] = (time(), result)
            return result
        return wrapper
    return decorator
```

## Time Complexity Optimization

### Efficient Data Structure Selection
```python
# O(n) lookup
items = [1, 2, 3, 4, 5]
if value in items:  # Linear search
    process(value)

# O(1) lookup
items_set = {1, 2, 3, 4, 5}
if value in items_set:  # Constant time
    process(value)

# Dictionary for O(1) lookups with metadata
items_dict = {item: metadata for item, metadata in pairs}
```

### Algorithm Choice Optimization
```python
from typing import List, Set

# O(n²) approach
def find_duplicates_simple(items: List[int]) -> List[int]:
    duplicates = []
    for i, item in enumerate(items):
        if item in items[i+1:]:  # O(n) lookup in slice
            duplicates.append(item)
    return duplicates

# O(n) approach
def find_duplicates_optimized(items: List[int]) -> List[int]:
    seen: Set[int] = set()
    duplicates: Set[int] = set()
    for item in items:  # Single pass
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return list(duplicates)
```

## Space-Time Tradeoffs

### In-Place vs New Allocation
```python
def reverse_string_extra_space(s: str) -> str:
    return s[::-1]  # Creates new string

def reverse_string_in_place(s: List[str]) -> None:
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
```

### Precomputation for Speed
```python
from typing import Dict, List

# Computing on demand
def get_factorial(n: int) -> int:
    if n <= 1:
        return 1
    return n * get_factorial(n - 1)

# Precomputed lookup table
FACTORIALS: Dict[int, int] = {0: 1}
def get_factorial_fast(n: int) -> int:
    if n in FACTORIALS:
        return FACTORIALS[n]
    for i in range(max(FACTORIALS.keys()) + 1, n + 1):
        FACTORIALS[i] = i * FACTORIALS[i - 1]
    return FACTORIALS[n]
```

## Parallelization and Concurrency

### Parallel Processing for CPU-bound Tasks
```python
from multiprocessing import Pool
from typing import List, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def parallel_map(func: Callable[[T], U], items: List[T], 
                chunk_size: int = None) -> List[U]:
    with Pool() as pool:
        return pool.map(func, items, chunk_size)

# Example usage
numbers = list(range(1000000))
squares = parallel_map(lambda x: x * x, numbers)
```

### Async IO for IO-bound Tasks
```python
import asyncio
from typing import List
import aiohttp

async def fetch_urls(urls: List[str]) -> List[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_url(session, url)
            for url in urls
        ]
        return await asyncio.gather(*tasks)

async def fetch_url(session: aiohttp.ClientSession, 
                   url: str) -> dict:
    async with session.get(url) as response:
        return await response.json()
```

## Profiling and Optimization

### Using cProfile
```python
import cProfile
import pstats
from pstats import SortKey

def profile_function(func: Callable) -> None:
    profiler = cProfile.Profile()
    profiler.enable()
    func()
    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats(SortKey.TIME)
    stats.print_stats()
```

### Memory Profiling
```python
from memory_profiler import profile

@profile
def memory_intensive_function() -> None:
    large_list = [i * i for i in range(1000000)]
    del large_list
```

## Best Practices

1. **Always Profile First**
   - Identify actual bottlenecks before optimizing
   - Use cProfile for time profiling
   - Use memory_profiler for memory profiling

2. **Choose Appropriate Data Structures**
   - Use sets for membership testing
   - Use dictionaries for key-value lookups
   - Use arrays (lists) for sequential access

3. **Optimize Inner Loops**
   - Move invariant computations outside loops
   - Use list comprehensions instead of loops where appropriate
   - Consider using numpy for numerical computations

4. **Use Built-in Functions**
   - Prefer map(), filter(), reduce() for functional operations
   - Use sorted() with key function instead of custom sort
   - Leverage itertools for efficient iterations

5. **Memory Management**
   - Use generators for large datasets
   - Implement cleanup for large objects
   - Consider using __slots__ for classes with fixed attributes

## Common Optimization Patterns

### String Concatenation
```python
# Inefficient: O(n²)
result = ""
for item in items:
    result += str(item)

# Efficient: O(n)
result = "".join(str(item) for item in items)
```

### List Operations
```python
# Inefficient: O(n) for each append
list1 = []
for item in items:
    list1.append(item)

# Efficient: O(n) total
list2 = [item for item in items]

# Efficient for known size
list3 = [None] * size
for i in range(size):
    list3[i] = compute_value(i)
```

### Dictionary Operations
```python
# Inefficient: Multiple lookups
if key in dict1:
    value = dict1[key]
    process(value)

# Efficient: Single lookup
value = dict1.get(key)
if value is not None:
    process(value)
```

## Exercises

1. Implement a cache decorator with size limit and timeout
2. Create a memory-efficient generator for processing large files
3. Optimize a recursive function using dynamic programming
4. Implement parallel processing for a CPU-intensive task
5. Profile and optimize a slow algorithm