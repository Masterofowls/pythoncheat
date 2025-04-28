# Functional Programming in Python

## First-Class Functions

### Functions as Objects
```python
def square(x: int) -> int:
    return x * x

def cube(x: int) -> int:
    return x * x * x

# Storing functions in variables
func = square
result = func(4)  # 16

# Functions in data structures
operations = [square, cube]
results = [func(3) for func in operations]  # [9, 27]
```

### Higher-Order Functions
```python
from typing import Callable, List

def apply_twice(func: Callable[[int], int], x: int) -> int:
    return func(func(x))

def create_multiplier(factor: int) -> Callable[[int], int]:
    def multiplier(x: int) -> int:
        return x * factor
    return multiplier

# Using higher-order functions
double = create_multiplier(2)
print(double(5))  # 10

triple = create_multiplier(3)
print(triple(5))  # 15
```

## Pure Functions

### Characteristics
```python
# Pure function - same input always gives same output
def add(x: int, y: int) -> int:
    return x + y

# Impure function - depends on external state
counter = 0
def increment() -> int:
    global counter
    counter += 1
    return counter
```

### Benefits of Pure Functions
```python
from typing import List

# Pure function - easy to test and reason about
def merge_sorted_lists(list1: List[int], list2: List[int]) -> List[int]:
    result = []
    i = j = 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] <= list2[j]:
            result.append(list1[i])
            i += 1
        else:
            result.append(list2[j])
            j += 1
    
    result.extend(list1[i:])
    result.extend(list2[j:])
    return result
```

## Built-in Functional Tools

### map()
```python
from typing import List, Callable, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def map_list(func: Callable[[T], U], items: List[T]) -> List[U]:
    return list(map(func, items))

# Examples
numbers = [1, 2, 3, 4, 5]
squares = map_list(lambda x: x * x, numbers)  # [1, 4, 9, 16, 25]
names = ["alice", "bob", "charlie"]
upper_names = map_list(str.upper, names)  # ["ALICE", "BOB", "CHARLIE"]
```

### filter()
```python
def filter_list(pred: Callable[[T], bool], items: List[T]) -> List[T]:
    return list(filter(pred, items))

# Examples
numbers = [1, 2, 3, 4, 5, 6]
even = filter_list(lambda x: x % 2 == 0, numbers)  # [2, 4, 6]
words = ["apple", "banana", "cherry", "date"]
long_words = filter_list(lambda x: len(x) > 5, words)  # ["banana"]
```

### reduce()
```python
from functools import reduce
from typing import Optional

def reduce_list(
    func: Callable[[T, T], T],
    items: List[T],
    initial: Optional[T] = None
) -> T:
    if initial is not None:
        return reduce(func, items, initial)
    return reduce(func, items)

# Examples
numbers = [1, 2, 3, 4, 5]
sum_all = reduce_list(lambda x, y: x + y, numbers)  # 15
product = reduce_list(lambda x, y: x * y, numbers)  # 120
```

## List Comprehensions

### Basic Comprehensions
```python
# List comprehension with transformation
squares = [x * x for x in range(10)]

# List comprehension with filtering
even_squares = [x * x for x in range(10) if x % 2 == 0]

# Nested list comprehension
matrix = [[i + j for j in range(3)] for i in range(3)]
```

### Advanced Comprehensions
```python
from typing import Dict, Set, Tuple

# Dictionary comprehension
square_dict: Dict[int, int] = {x: x * x for x in range(5)}

# Set comprehension
vowels = "aeiou"
word = "hello"
vowel_set: Set[str] = {c for c in word if c in vowels}

# Generator expression
sum_squares = sum(x * x for x in range(10))
```

## Immutability

### Immutable Data Structures
```python
from typing import NamedTuple, Tuple

class Point(NamedTuple):
    x: float
    y: float

    def move(self, dx: float, dy: float) -> 'Point':
        return Point(self.x + dx, self.y + dy)

def update_tuple(t: Tuple[int, ...], index: int, value: int) -> Tuple[int, ...]:
    return t[:index] + (value,) + t[index + 1:]
```

### Working with Immutable State
```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass(frozen=True)
class User:
    name: str
    email: str
    age: Optional[int] = None

    def with_age(self, new_age: int) -> 'User':
        return User(self.name, self.email, new_age)

    def with_email(self, new_email: str) -> 'User':
        return User(self.name, new_email, self.age)
```

## Function Composition

### Basic Composition
```python
from typing import Callable

def compose2(f: Callable[[U], V], g: Callable[[T], U]) -> Callable[[T], V]:
    return lambda x: f(g(x))

# Example
def double(x: int) -> int:
    return x * 2

def increment(x: int) -> int:
    return x + 1

double_then_increment = compose2(increment, double)
increment_then_double = compose2(double, increment)

print(double_then_increment(3))  # 7
print(increment_then_double(3))  # 8
```

### Advanced Composition
```python
from functools import reduce
from typing import Callable, TypeVar

T = TypeVar('T')

def compose(*functions: Callable[[T], T]) -> Callable[[T], T]:
    return reduce(lambda f, g: lambda x: f(g(x)), functions)

def pipe(*functions: Callable[[T], T]) -> Callable[[T], T]:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

# Example
def add_one(x: int) -> int:
    return x + 1

def multiply_by_two(x: int) -> int:
    return x * 2

def subtract_three(x: int) -> int:
    return x - 3

# Composition (right to left)
composed = compose(subtract_three, multiply_by_two, add_one)
print(composed(5))  # ((5 + 1) * 2) - 3 = 9

# Pipeline (left to right)
piped = pipe(add_one, multiply_by_two, subtract_three)
print(piped(5))  # ((5 + 1) * 2) - 3 = 9
```

## Exercises

1. Implement a functional linked list with immutable operations
2. Create a pipeline of data transformations using function composition
3. Write a memoization decorator for pure functions
4. Implement map, filter, and reduce from scratch
5. Create an immutable stack or queue data structure