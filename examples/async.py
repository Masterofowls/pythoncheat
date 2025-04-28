import asyncio
import aiohttp
import time

# Basic async function
async def basic_async_function():
    await asyncio.sleep(1)
    return "Done sleeping"

# Async function with multiple awaits
async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

# Parallel execution example
async def parallel_tasks():
    tasks = [
        asyncio.create_task(basic_async_function()),
        asyncio.create_task(basic_async_function())
    ]
    results = await asyncio.gather(*tasks)
    return results

# Async generator
async def async_generator():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i

# Main function demonstrating usage
async def main():
    # Basic async call
    result = await basic_async_function()
    print(f"Basic async result: {result}")
    
    # Parallel execution
    parallel_result = await parallel_tasks()
    print(f"Parallel results: {parallel_result}")
    
    # Using async generator
    async for number in async_generator():
        print(f"Generated: {number}")
    
    # Fetch data example (commented out as it requires internet)
    # data = await fetch_data('https://api.github.com')
    # print(data)

if __name__ == "__main__":
    # Run the async program
    asyncio.run(main())