import pytest

# Fixture example
@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

# Basic test function
def test_basic():
    assert True

# Test with fixture
def test_with_fixture(sample_data):
    assert len(sample_data) == 5
    assert sample_data[0] == 1

# Parameterized test
@pytest.mark.parametrize("input,expected", [
    (2, 4),
    (3, 6),
    (4, 8)
])
def test_multiplication(input, expected):
    assert input * 2 == expected

# Test that expects an exception
def test_zero_division():
    with pytest.raises(ZeroDivisionError):
        1 / 0

# Skip test example
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

# Conditional skip
@pytest.mark.skipif(True, reason="Condition not met")
def test_conditional():
    pass

# Custom marker
@pytest.mark.slow
def test_slow_operation():
    pass

# Setup and teardown using fixtures
@pytest.fixture(scope="module")
def database_connection():
    # Setup
    db = {"connected": True}
    yield db
    # Teardown
    db["connected"] = False

def test_database(database_connection):
    assert database_connection["connected"] == True

# Test class example
class TestClass:
    def test_method_one(self):
        assert 1 + 1 == 2
    
    def test_method_two(self):
        assert "hello".upper() == "HELLO"

# Fixture with multiple tests
@pytest.fixture
def complex_data():
    return {"name": "test", "value": 42}

def test_name(complex_data):
    assert complex_data["name"] == "test"

def test_value(complex_data):
    assert complex_data["value"] == 42