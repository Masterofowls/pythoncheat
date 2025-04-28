"""Tests for concurrent functional programming patterns."""
import asyncio
import pytest
from examples.concurrent_functional import (
    AsyncPipeline, ParallelMap, AsyncSuccess, AsyncFailure,
    AsyncHTTPClient, DataProcessor, RateLimiter, RateLimitedPipeline,
    with_backpressure
)

@pytest.mark.asyncio
async def test_async_pipeline():
    async def step1(x: int) -> int:
        return x * 2
    
    async def step2(x: int) -> str:
        return f"Result: {x}"
    
    pipeline = AsyncPipeline([step1, step2])
    result = await pipeline.process(5)
    assert result == "Result: 10"

def test_parallel_map():
    mapper = ParallelMap(max_workers=2)
    numbers = list(range(10))
    result = mapper.map(lambda x: x * 2, numbers)
    assert result == [x * 2 for x in numbers]

@pytest.mark.asyncio
async def test_async_result_success():
    success = AsyncSuccess(42)
    assert success.is_success()
    
    async def transform(x: int) -> str:
        return str(x)
    
    result = await success.map(transform)
    assert result.is_success()
    assert await result.run() == "42"

@pytest.mark.asyncio
async def test_async_result_failure():
    error = ValueError("test error")
    failure = AsyncFailure(error)
    assert not failure.is_success()
    assert failure.get_error() == error
    
    async def transform(x: int) -> str:
        return str(x)
    
    result = await failure.map(transform)
    assert not result.is_success()
    with pytest.raises(ValueError):
        await result.run()

@pytest.mark.asyncio
async def test_rate_limiter():
    limiter = RateLimiter(rate_limit=10)
    start_time = asyncio.get_event_loop().time()
    
    for _ in range(5):
        await limiter.acquire()
    
    elapsed = asyncio.get_event_loop().time() - start_time
    assert elapsed < 1.0  # Should complete quickly for only 5 requests

@pytest.mark.asyncio
async def test_rate_limited_pipeline():
    async def step(x: int) -> int:
        return x + 1
    
    pipeline = RateLimitedPipeline([step], rate_limit=10)
    results = await asyncio.gather(*(pipeline.process(i) for i in range(5)))
    assert results == [1, 2, 3, 4, 5]

@pytest.mark.asyncio
async def test_data_processor():
    processor = DataProcessor(chunk_size=2)
    data = list(range(5))
    
    def process(x: int) -> int:
        return x * 2
    
    results = processor.parallel_process(data, process)
    assert sorted(results) == [0, 2, 4, 6, 8]

@pytest.mark.asyncio
async def test_backpressure():
    async def generate():
        for i in range(5):
            yield i
            await asyncio.sleep(0.1)
    
    results = []
    async for item in with_backpressure(generate(), max_buffer=2):
        results.append(item)
    
    assert results == [0, 1, 2, 3, 4]

@pytest.mark.asyncio
async def test_http_client():
    client = AsyncHTTPClient(max_retries=2)
    try:
        # Test with a real API endpoint
        result = await client.fetch("https://jsonplaceholder.typicode.com/posts/1")
        assert result.is_success()
        data = await result.run()
        assert isinstance(data, dict)
        assert "id" in data
    finally:
        await client.close()

if __name__ == "__main__":
    pytest.main([__file__])