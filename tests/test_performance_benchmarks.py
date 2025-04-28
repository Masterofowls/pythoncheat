"""Tests for performance benchmarking examples"""
import pytest
from examples.performance_benchmarks import (
    DictCache,
    TimedDictCache,
    LRUCache,
    TestData,
    generate_test_data,
    benchmark_caches,
    benchmark_serialization,
    benchmark_string_operations
)
import json
from pathlib import Path
import time

def test_dict_cache():
    """Test basic dictionary cache"""
    cache = DictCache[TestData]()
    data = TestData(1, "test", {"value": 100})
    
    # Test set and get
    cache.set("test", data)
    result = cache.get("test")
    
    assert result is not None
    assert result.id == 1
    assert result.name == "test"
    assert result.data["value"] == 100

def test_timed_dict_cache():
    """Test timed dictionary cache"""
    cache = TimedDictCache[TestData](timeout=1)  # 1 second timeout
    data = TestData(1, "test", {"value": 100})
    
    # Test immediate get
    cache.set("test", data)
    result = cache.get("test")
    assert result is not None
    assert result.id == 1
    
    # Test timeout
    time.sleep(1.1)  # Wait for timeout
    result = cache.get("test")
    assert result is None

def test_lru_cache():
    """Test LRU cache"""
    cache = LRUCache[TestData](capacity=2)
    data1 = TestData(1, "test1", {"value": 100})
    data2 = TestData(2, "test2", {"value": 200})
    data3 = TestData(3, "test3", {"value": 300})
    
    # Fill cache
    cache.set("test1", data1)
    cache.set("test2", data2)
    
    # Access test1 to make it most recently used
    _ = cache.get("test1")
    
    # Add test3, should evict test2
    cache.set("test3", data3)
    
    assert cache.get("test1") is not None
    assert cache.get("test2") is None
    assert cache.get("test3") is not None

def test_test_data_generation():
    """Test test data generation"""
    data = generate_test_data(5)
    
    assert len(data) == 5
    assert all(isinstance(item, TestData) for item in data)
    assert all(item.id == i for i, item in enumerate(data))
    assert all(isinstance(item.data, dict) for item in data)

def test_benchmark_execution():
    """Test that benchmarks run without errors"""
    # Create output directory
    output_dir = Path("benchmark_results")
    output_dir.mkdir(exist_ok=True)
    
    # Run benchmarks
    benchmark_caches()
    benchmark_serialization()
    benchmark_string_operations()
    
    # Check that plot files were created
    assert (output_dir / "execution_times.png").exists()
    assert (output_dir / "memory_usage.png").exists()

def test_serialization_correctness():
    """Test that different serialization methods produce equivalent results"""
    test_data = TestData(1, "test", {"value": 100})
    
    # JSON dumps
    json_result = json.dumps({
        "id": test_data.id,
        "name": test_data.name,
        "data": test_data.data
    })
    
    # Manual dict
    manual_result = str({
        "id": test_data.id,
        "name": test_data.name,
        "data": test_data.data
    })
    
    # Dataclass dict
    dataclass_result = str({
        field: getattr(test_data, field)
        for field in ["id", "name", "data"]
    })
    
    # Convert all to dict for comparison
    json_dict = json.loads(json_result)
    manual_dict = eval(manual_result)  # Safe for test data
    dataclass_dict = eval(dataclass_result)  # Safe for test data
    
    assert json_dict["id"] == manual_dict["id"] == dataclass_dict["id"]
    assert json_dict["name"] == manual_dict["name"] == dataclass_dict["name"]
    assert json_dict["data"] == manual_dict["data"] == dataclass_dict["data"]

def test_string_operation_correctness():
    """Test that different string operations produce equivalent results"""
    test_strings = ["test_" * 2 for _ in range(3)]
    
    # Test different concatenation methods
    plus_result = ""
    for s in test_strings:
        plus_result = plus_result + s
    
    join_result = "".join(test_strings)
    
    fstring_result = ""
    for s in test_strings:
        fstring_result = f"{fstring_result}{s}"
    
    assert plus_result == join_result == fstring_result
    assert len(plus_result) == len(join_result) == len(fstring_result)