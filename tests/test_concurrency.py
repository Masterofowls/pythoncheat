"""Tests for concurrency examples"""
import pytest
import asyncio
from examples.concurrency_comparison import (
    fetch_url,
    cpu_intensive,
    threading_example,
    multiprocessing_example,
    asyncio_example,
    DataProcessor,
    URLS
)

def test_cpu_intensive():
    """Test CPU-intensive computation"""
    result = cpu_intensive(1000)
    assert result == sum(i * i for i in range(1000))
    assert result > 0

@pytest.mark.asyncio
async def test_asyncio_example():
    """Test asyncio implementation"""
    results = await asyncio_example()
    assert len(results) == len(URLS)
    assert all(isinstance(result, dict) for result in results)

def test_threading_example():
    """Test threading implementation"""
    results = threading_example()
    assert len(results) == len(URLS)
    assert all(isinstance(result, dict) for result in results)

def test_multiprocessing_example():
    """Test multiprocessing implementation"""
    results = multiprocessing_example()
    assert len(results) == 3  # We use 3 numbers in the example
    assert all(isinstance(result, int) for result in results)
    assert all(result > 0 for result in results)

def test_data_processor():
    """Test combined processing approach"""
    processor = DataProcessor(
        urls=URLS[:2],  # Use fewer URLs for testing
        numbers=[1000, 2000]  # Use smaller numbers for testing
    )
    processor.process_data()
    
    # Should have results from both URL fetching and CPU computation
    assert len(processor.results) == 4  # 2 URLs + 2 numbers
    # Results should be mix of dicts (from URLs) and ints (from CPU work)
    assert any(isinstance(result, dict) for result in processor.results)
    assert any(isinstance(result, int) for result in processor.results)