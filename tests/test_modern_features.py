"""Tests for modern Python features"""
import pytest
from decimal import Decimal
from datetime import datetime
import json
from examples.modern_features import (
    Cache,
    User,
    Product,
    PageIterator,
    process_command,
    AsyncResourceManager
)

def test_generic_cache():
    """Test generic cache implementation"""
    cache: Cache[User] = Cache[User](timeout=1)
    user = User("Test", "test@example.com", 25)
    
    # Test cache operations
    cache.set("test_user", user)
    cached = cache.get("test_user")
    assert cached is not None
    assert cached.name == "Test"
    assert cached.email == "test@example.com"
    
    # Test cache miss
    missing = cache.get("nonexistent")
    assert missing is None

def test_serializable_protocol():
    """Test Serializable protocol implementation"""
    user = User("Test", "test@example.com", 25, ["tag1", "tag2"])
    
    # Test serialization
    json_data = user.to_json()
    assert isinstance(json_data, str)
    
    # Test deserialization
    new_user = User("", "", 0)
    new_user.from_json(json_data)
    assert new_user.name == "Test"
    assert new_user.email == "test@example.com"
    assert new_user.age == 25
    assert new_user.tags == ["tag1", "tag2"]

def test_pattern_matching():
    """Test pattern matching command processing"""
    # Test valid commands
    assert "Creating user" in process_command("user create john john@example.com 30")
    assert "Listing all users" in process_command("user list")
    assert "Help for topics" in process_command("help user profile")
    
    # Test invalid command
    assert "Unknown command" in process_command("invalid command")

@pytest.mark.asyncio
async def test_async_resource_manager():
    """Test async resource management"""
    async with AsyncResourceManager("https://api.github.com") as manager:
        try:
            data = await manager.fetch_data()
            assert isinstance(data, dict)
        except Exception as e:
            pytest.skip(f"External API test failed: {e}")

def test_product_validation():
    """Test product validation and calculations"""
    # Test valid product
    product = Product("Test", Decimal("10.00"), 2, Decimal("10"))
    assert product.total_price == Decimal("18.00")  # 10 * 2 * 0.9
    
    # Test negative price
    with pytest.raises(ValueError):
        Product("Test", Decimal("-1.00"))
    
    # Test negative quantity
    with pytest.raises(ValueError):
        Product("Test", Decimal("10.00"), -1)
    
    # Test invalid discount
    with pytest.raises(ValueError):
        Product("Test", Decimal("10.00"), 1, Decimal("101"))

def test_pagination_iterator():
    """Test pagination iterator"""
    items = list(range(10))
    
    # Test with exact division
    paginator = PageIterator(items, page_size=2)
    pages = list(paginator)
    assert len(pages) == 5
    assert all(len(page) == 2 for page in pages[:4])
    
    # Test with remainder
    paginator = PageIterator(items, page_size=3)
    pages = list(paginator)
    assert len(pages) == 4
    assert len(pages[-1]) == 1

def test_cached_property():
    """Test cached property behavior"""
    product = Product("Test", Decimal("10.00"), 2, Decimal("10"))
    
    # First access calculates the value
    initial_total = product.total_price
    assert initial_total == Decimal("18.00")
    
    # Change quantity (shouldn't affect cached total)
    product.quantity = 3
    assert product.total_price == initial_total  # Still using cached value

def test_type_hints():
    """Test type hint compatibility"""
    # Test generic cache with different types
    string_cache: Cache[str] = Cache[str]()
    int_cache: Cache[int] = Cache[int]()
    
    string_cache.set("test", "value")
    int_cache.set("test", 42)
    
    assert string_cache.get("test") == "value"
    assert int_cache.get("test") == 42

def test_edge_cases():
    """Test edge cases and boundary conditions"""
    # Empty pagination
    paginator = PageIterator([], page_size=10)
    assert list(paginator) == []
    
    # Zero quantity product
    product = Product("Test", Decimal("10.00"), 0)
    assert product.total_price == 0
    
    # No discount product
    product = Product("Test", Decimal("10.00"), 1)
    assert product.total_price == Decimal("10.00")
    
    # Cache timeout
    cache = Cache[str](timeout=0)  # Immediate timeout
    cache.set("test", "value")
    assert cache.get("test") is None