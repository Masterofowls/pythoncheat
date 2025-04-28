"""Tests for benchmarking utilities"""
import pytest
import time
from pathlib import Path
from examples.benchmark_utils import (
    PerformanceBenchmark,
    benchmark,
    BenchmarkResult
)

def test_benchmark_function():
    """Test basic function benchmarking"""
    def test_func(n: int) -> int:
        time.sleep(0.1)  # Simulate work
        return n * n
    
    bench = PerformanceBenchmark(iterations=3)
    result = bench.benchmark_function(test_func, "test", 5)
    
    assert isinstance(result, BenchmarkResult)
    assert result.name == "test"
    assert len(result.execution_times) == 3
    assert all(t >= 0.1 for t in result.execution_times)
    assert result.mean_time >= 0.1
    assert result.peak_memory > 0

def test_compare_implementations():
    """Test comparing multiple implementations"""
    def impl1(n: int) -> list:
        return [i * 2 for i in range(n)]
    
    def impl2(n: int) -> list:
        result = []
        for i in range(n):
            result.append(i * 2)
        return result
    
    bench = PerformanceBenchmark(iterations=2)
    results = bench.compare_implementations(
        {
            "list_comp": impl1,
            "for_loop": impl2
        },
        1000
    )
    
    assert len(results) == 2
    assert "list_comp" in results
    assert "for_loop" in results
    assert all(isinstance(r, BenchmarkResult) for r in results.values())

def test_benchmark_decorator():
    """Test the benchmark decorator"""
    @benchmark(iterations=2)
    def test_func(n: int) -> int:
        return sum(i * i for i in range(n))
    
    result = test_func(1000)
    assert result == sum(i * i for i in range(1000))

def test_result_plotting(tmp_path):
    """Test benchmark result plotting"""
    def test_func(n: int) -> int:
        return n * n
    
    bench = PerformanceBenchmark(iterations=2)
    bench.benchmark_function(test_func, "test", 5)
    
    # Test plot generation
    bench.plot_results(tmp_path)
    
    assert (tmp_path / "execution_times.png").exists()
    assert (tmp_path / "memory_usage.png").exists()

def test_result_saving(tmp_path):
    """Test saving benchmark results"""
    def test_func(n: int) -> int:
        return n * n
    
    bench = PerformanceBenchmark(iterations=2)
    bench.benchmark_function(test_func, "test", 5)
    
    results_file = tmp_path / "results.json"
    bench.save_results(results_file)
    
    assert results_file.exists()
    assert results_file.stat().st_size > 0

def test_memory_tracking():
    """Test memory usage tracking"""
    def memory_intensive() -> list:
        return [i * i for i in range(100000)]
    
    bench = PerformanceBenchmark(iterations=2)
    result = bench.benchmark_function(memory_intensive, "memory_test")
    
    assert result.peak_memory > 0
    assert len(result.memory_samples) == 2
    assert all(sample > 0 for sample in result.memory_samples)

@pytest.mark.asyncio
async def test_async_function_benchmark():
    """Test benchmarking async functions"""
    async def async_func(n: int) -> int:
        await asyncio.sleep(0.1)
        return n * n
    
    bench = PerformanceBenchmark(iterations=2)
    result = bench.benchmark_function(
        lambda x: asyncio.run(async_func(x)),
        "async_test",
        5
    )
    
    assert result.mean_time >= 0.1
    assert result.peak_memory > 0