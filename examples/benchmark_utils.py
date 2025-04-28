"""
Benchmarking utilities for measuring performance optimizations.
Provides tools to measure execution time, memory usage, and compare implementations.
"""
import time
import statistics
import gc
import sys
import tracemalloc
from typing import Callable, List, Dict, Any, TypeVar, Tuple
from dataclasses import dataclass
from functools import wraps
import matplotlib.pyplot as plt
from pathlib import Path
import json

T = TypeVar('T')
R = TypeVar('R')

@dataclass
class BenchmarkResult:
    """Stores results of a benchmark run"""
    name: str
    execution_times: List[float]
    mean_time: float
    median_time: float
    std_dev: float
    peak_memory: int
    memory_samples: List[int]

class PerformanceBenchmark:
    """Utility for running performance benchmarks"""
    
    def __init__(self, iterations: int = 5):
        self.iterations = iterations
        self.results: Dict[str, BenchmarkResult] = {}
    
    def benchmark_function(self, 
                         func: Callable[..., R],
                         name: str,
                         *args,
                         **kwargs) -> BenchmarkResult:
        """Run benchmark on a function with given arguments"""
        execution_times = []
        memory_samples = []
        
        # Enable memory tracking
        tracemalloc.start()
        
        # Run multiple iterations
        for _ in range(self.iterations):
            # Clear any cached data
            gc.collect()
            
            # Measure execution time
            start_time = time.perf_counter()
            func(*args, **kwargs)
            end_time = time.perf_counter()
            execution_times.append(end_time - start_time)
            
            # Measure memory usage
            current, peak = tracemalloc.get_traced_memory()
            memory_samples.append(current)
        
        tracemalloc.stop()
        
        # Calculate statistics
        result = BenchmarkResult(
            name=name,
            execution_times=execution_times,
            mean_time=statistics.mean(execution_times),
            median_time=statistics.median(execution_times),
            std_dev=statistics.stdev(execution_times) if len(execution_times) > 1 else 0,
            peak_memory=max(memory_samples),
            memory_samples=memory_samples
        )
        
        self.results[name] = result
        return result
    
    def compare_implementations(self, 
                              implementations: Dict[str, Callable],
                              *args,
                              **kwargs) -> Dict[str, BenchmarkResult]:
        """Compare multiple implementations of the same functionality"""
        for name, func in implementations.items():
            self.benchmark_function(func, name, *args, **kwargs)
        return self.results
    
    def plot_results(self, save_path: Path = None) -> None:
        """Generate performance comparison plots"""
        # Execution time comparison
        plt.figure(figsize=(10, 6))
        names = list(self.results.keys())
        times = [result.mean_time for result in self.results.values()]
        plt.bar(names, times)
        plt.title('Execution Time Comparison')
        plt.ylabel('Time (seconds)')
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path / 'execution_times.png')
        plt.close()
        
        # Memory usage comparison
        plt.figure(figsize=(10, 6))
        memory_usage = [result.peak_memory / 1024 / 1024 for result in self.results.values()]
        plt.bar(names, memory_usage)
        plt.title('Peak Memory Usage Comparison')
        plt.ylabel('Memory (MB)')
        plt.xticks(rotation=45)
        
        if save_path:
            plt.savefig(save_path / 'memory_usage.png')
        plt.close()
    
    def save_results(self, filepath: Path) -> None:
        """Save benchmark results to JSON file"""
        results_dict = {
            name: {
                'mean_time': result.mean_time,
                'median_time': result.median_time,
                'std_dev': result.std_dev,
                'peak_memory_mb': result.peak_memory / 1024 / 1024,
                'execution_times': result.execution_times,
                'memory_samples': result.memory_samples
            }
            for name, result in self.results.items()
        }
        
        with open(filepath, 'w') as f:
            json.dump(results_dict, f, indent=2)

def benchmark(iterations: int = 5):
    """Decorator for benchmarking functions"""
    def decorator(func: Callable[..., R]) -> Callable[..., R]:
        benchmark = PerformanceBenchmark(iterations=iterations)
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = benchmark.benchmark_function(func, func.__name__, *args, **kwargs)
            print(f"\nBenchmark results for {func.__name__}:")
            print(f"Mean execution time: {result.mean_time:.6f} seconds")
            print(f"Peak memory usage: {result.peak_memory / 1024 / 1024:.2f} MB")
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

# Example usage
def demonstrate_benchmarking():
    """Demonstrate usage of benchmarking utilities"""
    
    # Example functions to benchmark
    def implementation1(n: int) -> List[int]:
        return [i * i for i in range(n)]
    
    def implementation2(n: int) -> List[int]:
        result = []
        for i in range(n):
            result.append(i * i)
        return result
    
    # Create benchmark instance
    benchmark = PerformanceBenchmark(iterations=5)
    
    # Compare implementations
    results = benchmark.compare_implementations(
        {
            'list_comprehension': implementation1,
            'for_loop': implementation2
        },
        1000000
    )
    
    # Generate and save plots
    output_dir = Path('benchmark_results')
    output_dir.mkdir(exist_ok=True)
    benchmark.plot_results(output_dir)
    benchmark.save_results(output_dir / 'results.json')
    
    # Print results summary
    for name, result in results.items():
        print(f"\n{name}:")
        print(f"Mean time: {result.mean_time:.6f} seconds")
        print(f"Peak memory: {result.peak_memory / 1024 / 1024:.2f} MB")

if __name__ == '__main__':
    demonstrate_benchmarking()