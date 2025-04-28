"""Tests for functional programming patterns"""
import pytest
from datetime import datetime
from pathlib import Path
import json
import tempfile
from examples.functional_patterns import (
    DataPipeline,
    LogEntry,
    LogProcessor,
    Result,
    LazyPipeline
)

def test_data_pipeline():
    """Test generic data pipeline"""
    # Simple transformation pipeline
    pipeline = DataPipeline[int, str]([
        lambda x: x * 2,
        lambda x: x + 1,
        str
    ])
    
    result = pipeline.process(5)
    assert result == "11"
    
    # Test error handling
    def failing_step(x: int) -> int:
        raise ValueError("Test error")
    
    error_pipeline = DataPipeline([failing_step])
    result = error_pipeline.process(5)
    assert "error" in result
    assert result["type"] == "ValueError"

def test_log_processor():
    """Test log processing functionality"""
    # Valid log entry
    log_line = "2025-04-28T10:15:30 | ERROR | Test error | {\"id\": 123}"
    log_entry = LogProcessor.parse_log(log_line)
    
    assert isinstance(log_entry, LogEntry)
    assert log_entry.level == "ERROR"
    assert log_entry.message == "Test error"
    assert log_entry.metadata["id"] == 123
    
    # Test filtering
    assert LogProcessor.filter_errors(log_entry) == True
    
    # Test enrichment
    enriched = LogProcessor.enrich_metadata(log_entry)
    assert "processed_at" in enriched.metadata
    assert "severity" in enriched.metadata
    
    # Test formatting
    formatted = LogProcessor.format_output(enriched)
    assert isinstance(formatted, dict)
    assert all(k in formatted for k in ['time', 'level', 'message', 'metadata'])

def test_result_monad():
    """Test Result monad for error handling"""
    # Test successful case
    def safe_divide(x: float, y: float) -> Result[float]:
        if y == 0:
            return Result.failure(ZeroDivisionError("Division by zero"))
        return Result.success(x / y)
    
    result = safe_divide(10, 2)
    assert result.is_success()
    assert result._value == 5
    
    # Test error case
    result = safe_divide(10, 0)
    assert not result.is_success()
    assert isinstance(result.get_error(), ZeroDivisionError)
    
    # Test chaining
    def multiply_by_two(x: float) -> Result[float]:
        return Result.success(x * 2)
    
    chained = safe_divide(10, 2).bind(multiply_by_two)
    assert chained.is_success()
    assert chained._value == 10
    
    # Test mapping
    mapped = safe_divide(10, 2).map(lambda x: x * 2)
    assert mapped.is_success()
    assert mapped._value == 10

def test_lazy_pipeline():
    """Test lazy evaluation pipeline"""
    # Create test data file
    test_data = [
        {"id": 1, "value": 10},
        {"id": 2, "value": 20},
        {"invalid": "data"},
        {"id": 3, "value": 30}
    ]
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        for item in test_data:
            f.write(json.dumps(item) + "\n")
    
    try:
        pipeline = LazyPipeline()
        # Test reading
        lines = list(pipeline.read_lines(Path(f.name)))
        assert len(lines) == 4
        
        # Test JSON parsing
        parsed = list(pipeline.parse_json(lines))
        assert len(parsed) == 4
        
        # Test filtering
        filtered = list(pipeline.filter_valid(parsed))
        assert len(filtered) == 3  # One invalid record removed
        assert all('id' in item and 'value' in item for item in filtered)
        
        # Test transformation
        transformed = list(pipeline.transform(filtered))
        assert len(transformed) == 3
        assert all('processed_value' in item for item in transformed)
        assert transformed[0]['processed_value'] == 20  # 10 * 2
    
    finally:
        Path(f.name).unlink()  # Cleanup

def test_pipeline_composition():
    """Test composing multiple pipelines"""
    # Create pipelines
    number_pipeline = DataPipeline[int, int]([
        lambda x: x * 2,
        lambda x: x + 1
    ])
    
    string_pipeline = DataPipeline[int, str]([
        str,
        lambda x: f"Result: {x}"
    ])
    
    # Compose pipelines
    combined_steps = number_pipeline.steps + string_pipeline.steps
    combined = DataPipeline(combined_steps)
    
    result = combined.process(5)
    assert result == "Result: 11"

def test_error_propagation():
    """Test error handling and propagation"""
    def validate_positive(x: int) -> Result[int]:
        if x > 0:
            return Result.success(x)
        return Result.failure(ValueError("Number must be positive"))
    
    def double(x: int) -> Result[int]:
        return Result.success(x * 2)
    
    # Test successful chain
    result = validate_positive(5).bind(double)
    assert result.is_success()
    assert result._value == 10
    
    # Test error chain
    result = validate_positive(-5).bind(double)
    assert not result.is_success()
    assert isinstance(result.get_error(), ValueError)

def test_advanced_pipeline_features():
    """Test advanced features of data pipeline"""
    # Test pipeline with custom error handler
    def custom_handler(error: Exception) -> str:
        return f"Custom error: {str(error)}"
    
    pipeline = DataPipeline[int, str](
        steps=[lambda x: x if x > 0 else ValueError("Invalid input")],
        error_handler=custom_handler
    )
    
    result = pipeline.process(-5)
    assert result.startswith("Custom error")
    
    # Test pipeline step addition
    pipeline = pipeline.add_step(lambda x: str(x))
    assert callable(pipeline.steps[-1])