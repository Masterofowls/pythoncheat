# Python Design Patterns

## Creational Patterns

### Singleton
```python
from typing import Optional
from threading import Lock

class ThreadSafeSingleton:
    _instance: Optional['ThreadSafeSingleton'] = None
    _lock = Lock()
    
    def __new__(cls) -> 'ThreadSafeSingleton':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance
```

### Factory Method
```python
from abc import ABC, abstractmethod
from typing import Protocol

class Document(Protocol):
    def create(self) -> None: ...

class PDFDocument:
    def create(self) -> None:
        print("Creating PDF document")

class DocxDocument:
    def create(self) -> None:
        print("Creating DOCX document")

class DocumentFactory(ABC):
    @abstractmethod
    def create_document(self) -> Document:
        pass

class PDFFactory(DocumentFactory):
    def create_document(self) -> Document:
        return PDFDocument()

class DocxFactory(DocumentFactory):
    def create_document(self) -> Document:
        return DocxDocument()
```

## Structural Patterns

### Adapter
```python
from typing import Protocol, Any

class Target(Protocol):
    def request(self) -> str: ...

class Adaptee:
    def specific_request(self) -> str:
        return "Specific request"

class Adapter:
    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee
    
    def request(self) -> str:
        return f"Adapted: {self.adaptee.specific_request()}"
```

### Decorator
```python
from typing import Callable, Any
from functools import wraps
import time

def timer(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

@timer
def expensive_operation() -> None:
    time.sleep(1)
```

## Behavioral Patterns

### Observer
```python
from typing import List, Protocol
from abc import ABC, abstractmethod

class Observer(Protocol):
    def update(self, message: str) -> None: ...

class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)

class ConcreteSubject(Subject):
    def change_state(self, message: str) -> None:
        self.notify(message)
```

### Strategy
```python
from typing import Protocol, List
from dataclasses import dataclass

class SortStrategy(Protocol):
    def sort(self, data: List[int]) -> List[int]: ...

@dataclass
class QuickSort:
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

@dataclass
class MergeSort:
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result
```

## Modern Design Pattern Implementations

### Dependency Injection
```python
from typing import Protocol, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

class Database(Protocol):
    def save(self, data: Any) -> None: ...
    def load(self, id: str) -> Any: ...

class PostgresDB:
    def save(self, data: Any) -> None:
        print(f"Saving {data} to PostgreSQL")
    
    def load(self, id: str) -> Any:
        print(f"Loading {id} from PostgreSQL")

class MongoDBDatabase:
    def save(self, data: Any) -> None:
        print(f"Saving {data} to MongoDB")
    
    def load(self, id: str) -> Any:
        print(f"Loading {id} from MongoDB")

@dataclass
class UserRepository:
    database: Database
    
    def save_user(self, user: Any) -> None:
        self.database.save(user)
    
    def load_user(self, id: str) -> Any:
        return self.database.load(id)
```

### Repository Pattern
```python
from typing import Protocol, List, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class User:
    id: str
    name: str
    email: str

class UserRepository(Protocol):
    def get(self, id: str) -> Optional[User]: ...
    def save(self, user: User) -> None: ...
    def delete(self, id: str) -> None: ...
    def find_by_email(self, email: str) -> Optional[User]: ...

class PostgresUserRepository:
    def get(self, id: str) -> Optional[User]:
        # Implementation for PostgreSQL
        pass
    
    def save(self, user: User) -> None:
        # Implementation for PostgreSQL
        pass
    
    def delete(self, id: str) -> None:
        # Implementation for PostgreSQL
        pass
    
    def find_by_email(self, email: str) -> Optional[User]:
        # Implementation for PostgreSQL
        pass
```

### Unit of Work Pattern
```python
from typing import Protocol, Any, List
from contextlib import contextmanager
from dataclasses import dataclass

class UnitOfWork(Protocol):
    def commit(self) -> None: ...
    def rollback(self) -> None: ...

@dataclass
class PostgresUnitOfWork:
    def __init__(self) -> None:
        self.changes: List[Any] = []
    
    def commit(self) -> None:
        for change in self.changes:
            print(f"Committing {change}")
        self.changes.clear()
    
    def rollback(self) -> None:
        self.changes.clear()

@contextmanager
def unit_of_work(uow: UnitOfWork):
    try:
        yield uow
        uow.commit()
    except Exception:
        uow.rollback()
        raise
```

## Best Practices

1. Use Protocol for Interface Definitions
   - Prefer Protocol over ABC when possible
   - Enables structural subtyping
   - Better type checking support

2. Leverage Type Hints
   - Use generics for flexible implementations
   - Add type hints to all public interfaces
   - Use TypeVar for generic type constraints

3. Consider Immutability
   - Use @dataclass(frozen=True) for immutable data
   - Return new instances instead of modifying state
   - Use tuples for fixed-size collections

4. Follow SOLID Principles
   - Single Responsibility Principle
   - Open/Closed Principle
   - Liskov Substitution Principle
   - Interface Segregation Principle
   - Dependency Inversion Principle

## Pattern Usage Guidelines

1. Choose Patterns Carefully
   - Don't overuse patterns
   - Consider simpler solutions first
   - Patterns should solve specific problems

2. Modern Python Features
   - Use dataclasses for data containers
   - Leverage context managers
   - Use async patterns when appropriate

3. Testing Considerations
   - Patterns should make testing easier
   - Use dependency injection for testability
   - Mock interfaces rather than implementations