"""
Practical examples of functional programming patterns in Python.
Demonstrates real-world applications of functional concepts.
"""
from typing import (
    TypeVar, Generic, Callable, List, Dict, Optional, 
    Iterator, Iterable, Any, Union, Tuple
)
from dataclasses import dataclass, field
from functools import reduce, partial, wraps
import asyncio
from datetime import datetime
import json
from pathlib import Path
import time

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

# Practical Data Processing Pipeline
class DataPipeline(Generic[T, U]):
    """
    Generic data processing pipeline with type safety and error handling.
    """
    def __init__(self, 
                 steps: List[Callable[[T], U]] = None, 
                 error_handler: Callable[[Exception], U] = None):
        self.steps = steps or []
        self.error_handler = error_handler or self._default_error_handler
    
    def add_step(self, step: Callable[[T], U]) -> 'DataPipeline[T, U]':
        """Add a processing step to the pipeline"""
        return DataPipeline(self.steps + [step], self.error_handler)
    
    def process(self, data: T) -> U:
        """Process data through the pipeline"""
        try:
            return reduce(lambda d, step: step(d), self.steps, data)
        except Exception as e:
            return self.error_handler(e)
    
    @staticmethod
    def _default_error_handler(error: Exception) -> Any:
        """Default error handling"""
        return {
            'error': str(error),
            'type': error.__class__.__name__
        }

# Real-world example: Log Processing Pipeline
@dataclass
class LogEntry:
    """Log entry data structure"""
    timestamp: datetime
    level: str
    message: str
    metadata: Dict[str, Any] = field(default_factory=dict)

class LogProcessor:
    """Process log entries using functional patterns"""
    
    @staticmethod
    def parse_log(line: str) -> LogEntry:
        """Parse log line into structured data"""
        try:
            parts = line.split(" | ")
            return LogEntry(
                timestamp=datetime.fromisoformat(parts[0]),
                level=parts[1],
                message=parts[2],
                metadata=json.loads(parts[3]) if len(parts) > 3 else {}
            )
        except Exception as e:
            raise ValueError(f"Invalid log format: {str(e)}")
    
    @staticmethod
    def filter_errors(entry: LogEntry) -> bool:
        """Filter for error entries"""
        return entry.level.upper() == "ERROR"
    
    @staticmethod
    def enrich_metadata(entry: LogEntry) -> LogEntry:
        """Add additional metadata"""
        entry.metadata.update({
            'processed_at': datetime.now().isoformat(),
            'severity': 'high' if 'critical' in entry.message.lower() else 'normal'
        })
        return entry
    
    @staticmethod
    def format_output(entry: LogEntry) -> Dict[str, Any]:
        """Format entry for output"""
        return {
            'time': entry.timestamp.isoformat(),
            'level': entry.level,
            'message': entry.message,
            'metadata': entry.metadata
        }

# Example: Result Monad for Error Handling
@dataclass
class Result(Generic[T]):
    """Result monad for error handling"""
    _value: Optional[T] = None
    _error: Optional[Exception] = None
    
    @staticmethod
    def success(value: T) -> 'Result[T]':
        """Create successful result"""
        return Result(_value=value)
    
    @staticmethod
    def failure(error: Exception) -> 'Result[T]':
        """Create failed result"""
        return Result(_error=error)
    
    def bind(self, f: Callable[[T], 'Result[U]']) -> 'Result[U]':
        """Chain operations"""
        if self._error:
            return Result(_error=self._error)
        try:
            return f(self._value)
        except Exception as e:
            return Result(_error=e)
    
    def map(self, f: Callable[[T], U]) -> 'Result[U]':
        """Transform value while preserving result context"""
        return self.bind(lambda x: Result.success(f(x)))
    
    def get_or_else(self, default: T) -> T:
        """Get value or return default"""
        return self._value if self._value is not None else default
    
    def is_success(self) -> bool:
        """Check if result is successful"""
        return self._error is None
    
    def get_error(self) -> Optional[Exception]:
        """Get error if present"""
        return self._error

# Example: Lazy Evaluation with Generator Pipeline
class LazyPipeline:
    """Pipeline for lazy data processing"""
    
    @staticmethod
    def read_lines(file_path: Path) -> Iterator[str]:
        """Lazy file reading"""
        with open(file_path) as f:
            for line in f:
                yield line.strip()
    
    @staticmethod
    def parse_json(lines: Iterator[str]) -> Iterator[Dict]:
        """Parse JSON strings"""
        for line in lines:
            try:
                yield json.loads(line)
            except json.JSONDecodeError:
                continue
    
    @staticmethod
    def filter_valid(data: Iterator[Dict]) -> Iterator[Dict]:
        """Filter valid records"""
        for item in data:
            if all(k in item for k in ['id', 'value']):
                yield item
    
    @staticmethod
    def transform(data: Iterator[Dict]) -> Iterator[Dict]:
        """Transform records"""
        for item in data:
            yield {
                'id': item['id'],
                'processed_value': item['value'] * 2,
                'timestamp': datetime.now().isoformat()
            }

# Practical Examples
def demonstrate_patterns():
    """Demonstrate functional patterns with practical examples"""
    
    # Log Processing Example
    log_pipeline = DataPipeline[str, Dict]([
        LogProcessor.parse_log,
        LogProcessor.enrich_metadata,
        LogProcessor.format_output
    ])
    
    log_entry = "2025-04-28T10:15:30 | ERROR | Database connection failed | {}"
    result = log_pipeline.process(log_entry)
    print("\nProcessed Log Entry:", result)
    
    # Result Monad Example
    def divide(x: float, y: float) -> Result[float]:
        try:
            return Result.success(x / y)
        except ZeroDivisionError as e:
            return Result.failure(e)
    
    def calculate_percentage(value: float) -> Result[float]:
        return Result.success(value * 100)
    
    # Chain operations safely
    calculation = (divide(10, 2)
                  .bind(calculate_percentage)
                  .map(lambda x: f"{x}%"))
    print("\nCalculation Result:", calculation._value)
    
    # Lazy Pipeline Example
    def process_data_file(file_path: Path) -> Iterator[Dict]:
        pipeline = LazyPipeline()
        return pipeline.transform(
            pipeline.filter_valid(
                pipeline.parse_json(
                    pipeline.read_lines(file_path)
                )
            )
        )
    
    # Example with error handling using Result
    def safe_process(file_path: Path) -> Result[List[Dict]]:
        try:
            return Result.success(list(process_data_file(file_path)))
        except Exception as e:
            return Result.failure(e)

if __name__ == '__main__':
    demonstrate_patterns()