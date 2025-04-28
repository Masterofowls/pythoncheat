"""Tests for optimization examples"""
import pytest
import asyncio
import time
from pathlib import Path
from examples.optimization_examples import (
    DataPoint,
    DataProcessor,
    FileProcessor,
    ParallelProcessor,
    APIClient
)

def test_data_processor_optimization():
    """Test that optimized processing is faster than simple processing"""
    processor = DataProcessor()
    data_points = [
        DataPoint(i % 5, float(i), {"test": f"data_{i}"})
        for i in range(20)
    ]
    
    # Time unoptimized version
    start = time.time()
    simple_result = processor.process_data_simple(data_points)
    simple_time = time.time() - start
    
    # Time optimized version
    start = time.time()
    optimized_result = processor.process_data_optimized(data_points)
    optimized_time = time.time() - start
    
    # Verify results are the same
    assert simple_result == optimized_result
    # Verify optimization improves performance
    assert optimized_time < simple_time

def test_parallel_processing():
    """Test that parallel processing is faster for CPU-bound tasks"""
    items = [1000000 + i for i in range(4)]
    processor = ParallelProcessor()
    
    # Time serial processing
    start = time.time()
    serial_result = processor.process_data_serial(items)
    serial_time = time.time() - start
    
    # Time parallel processing
    start = time.time()
    parallel_result = processor.process_data_parallel(items)
    parallel_time = time.time() - start
    
    # Verify results are the same
    assert serial_result == parallel_result
    # Verify parallel processing is faster
    assert parallel_time < serial_time

def test_file_processor(tmp_path):
    """Test memory-efficient file processing"""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_data = "\n".join(str(i) for i in range(1000))
    test_file.write_text(test_data)
    
    processor = FileProcessor()
    
    # Test simple processing
    simple_result = processor.process_file_simple(test_file)
    assert len(simple_result) == 1000
    
    # Test generator processing
    gen_result = list(processor.process_file_generator(test_file))
    assert gen_result == simple_result

@pytest.mark.asyncio
async def test_concurrent_file_processing(tmp_path):
    """Test concurrent file processing"""
    # Create test files
    files = []
    for i in range(3):
        path = tmp_path / f"test_{i}.txt"
        path.write_text(f"content_{i}")
        files.append(path)
    
    processor = FileProcessor()
    results = await processor.process_files_async(files)
    
    assert len(results) == 3
    assert all(f"content_{i}" in results[i] for i in range(3))

@pytest.mark.asyncio
async def test_api_client():
    """Test API client optimizations"""
    client = APIClient("https://api.example.com")
    endpoints = ["users", "posts", "comments"]
    
    # Mock the API responses for testing
    async def mock_fetch_endpoint(*args, **kwargs):
        return {"data": "mock"}
    
    # Replace real fetch with mock
    client.fetch_endpoint = mock_fetch_endpoint
    
    results = await client.fetch_data_concurrent(endpoints)
    assert len(results) == 3
    assert all(result["data"] == "mock" for result in results)

def test_memory_usage():
    """Test memory usage patterns"""
    processor = FileProcessor()
    
    # Create large test data
    data = [str(i) for i in range(1000000)]
    
    # Test generator memory efficiency
    count = 0
    for _ in processor.process_file_generator(data):
        count += 1
    
    assert count == 1000000