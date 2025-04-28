"""
Common data structure operations and patterns in Python.
These snippets demonstrate practical uses of Python's built-in data structures.
"""
from typing import TypeVar, List, Dict, Set, Tuple, Optional
from collections import defaultdict, Counter, deque
from dataclasses import dataclass
from functools import reduce

T = TypeVar('T')

# List Operations
def list_operations() -> None:
    """Common list operations and patterns"""
    # List comprehension with filtering
    numbers = [1, 2, 3, 4, 5, 6]
    evens = [n for n in numbers if n % 2 == 0]
    
    # Flatten nested list
    nested = [[1, 2], [3, 4], [5, 6]]
    flattened = [item for sublist in nested for item in sublist]
    
    # Find duplicates
    items = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    duplicates = [item for item in set(items) 
                 if items.count(item) > 1]
    
    # Remove duplicates while maintaining order
    unique_ordered = list(dict.fromkeys(items))
    
    # Chunk a list
    def chunk_list(lst: List[T], size: int) -> List[List[T]]:
        return [lst[i:i + size] for i in range(0, len(lst), size)]

# Dictionary Operations
def dict_operations() -> None:
    """Common dictionary operations and patterns"""
    # Merge dictionaries
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    merged = {**dict1, **dict2}
    
    # Group items by key
    items = [('A', 1), ('B', 2), ('A', 3), ('B', 4)]
    grouped = defaultdict(list)
    for key, value in items:
        grouped[key].append(value)
    
    # Dictionary comprehension
    numbers = [1, 2, 3, 4, 5]
    squares = {n: n**2 for n in numbers}
    
    # Sort dictionary by value
    unsorted = {'b': 2, 'a': 3, 'c': 1}
    sorted_dict = dict(sorted(unsorted.items(), 
                            key=lambda x: x[1]))

# Set Operations
def set_operations() -> None:
    """Common set operations and patterns"""
    set1 = {1, 2, 3, 4, 5}
    set2 = {4, 5, 6, 7, 8}
    
    # Set operations
    union = set1 | set2
    intersection = set1 & set2
    difference = set1 - set2
    symmetric_diff = set1 ^ set2
    
    # Find unique elements
    items = [1, 2, 2, 3, 3, 3, 4, 5, 5]
    unique_items = set(items)
    
    # Check if all elements are unique
    def all_unique(lst: List[T]) -> bool:
        return len(lst) == len(set(lst))

# Tuple Operations
def tuple_operations() -> None:
    """Common tuple operations and patterns"""
    # Named tuple using dataclass
    @dataclass(frozen=True)
    class Point:
        x: float
        y: float
    
    # Tuple unpacking
    numbers = [(1, 2), (3, 4), (5, 6)]
    x_coords, y_coords = zip(*numbers)
    
    # Multiple assignment
    a, b, *rest = [1, 2, 3, 4, 5]
    first, *middle, last = [1, 2, 3, 4, 5]

# Collections Module Examples
def collections_examples() -> None:
    """Examples using collections module"""
    # Counter for counting elements
    text = "hello world"
    char_count = Counter(text)
    most_common = char_count.most_common(2)
    
    # DefaultDict for automatic default values
    word_lengths = defaultdict(int)
    for word in ["hello", "world", "python"]:
        word_lengths[word] = len(word)
    
    # Deque for efficient queue operations
    queue = deque(maxlen=3)  # Fixed-size queue
    for i in range(5):
        queue.append(i)  # Automatically removes oldest

# Advanced Data Structure Patterns
def advanced_patterns() -> None:
    """Advanced patterns with data structures"""
    # Priority queue using heapq
    import heapq
    
    class PriorityQueue:
        def __init__(self):
            self._queue = []
            self._index = 0
        
        def push(self, item: T, priority: int) -> None:
            heapq.heappush(self._queue, 
                          (-priority, self._index, item))
            self._index += 1
        
        def pop(self) -> Optional[T]:
            if not self._queue:
                return None
            return heapq.heappop(self._queue)[-1]
    
    # Bi-directional mapping
    class BiDict:
        def __init__(self):
            self._forward = {}
            self._backward = {}
        
        def add(self, key: T, value: T) -> None:
            self._forward[key] = value
            self._backward[value] = key
        
        def get_key(self, value: T) -> Optional[T]:
            return self._backward.get(value)
        
        def get_value(self, key: T) -> Optional[T]:
            return self._forward.get(key)

# Cache Implementation
def cache_examples() -> None:
    """Different cache implementation patterns"""
    # LRU Cache
    from functools import lru_cache
    
    @lru_cache(maxsize=128)
    def fibonacci(n: int) -> int:
        if n < 2:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)
    
    # Time-based cache
    from time import time
    
    class TimedCache:
        def __init__(self, timeout: int):
            self.timeout = timeout
            self.cache: Dict[str, Tuple[float, Any]] = {}
        
        def get(self, key: str) -> Optional[Any]:
            if key in self.cache:
                timestamp, value = self.cache[key]
                if time() - timestamp < self.timeout:
                    return value
                del self.cache[key]
            return None
        
        def set(self, key: str, value: Any) -> None:
            self.cache[key] = (time(), value)

if __name__ == '__main__':
    # Example usage
    list_operations()
    dict_operations()
    set_operations()
    tuple_operations()
    collections_examples()
    advanced_patterns()
    cache_examples()