"""Tests for advanced algorithm implementations"""
import pytest
from datetime import datetime, timedelta
from examples.advanced_algorithms import (
    TextSearchEngine,
    RoutePlanner,
    DataStreamAnalyzer
)

def test_text_search_engine():
    """Test text search functionality"""
    engine = TextSearchEngine()
    
    # Add test documents
    doc1 = "Python is a great programming language for data science"
    doc2 = "Data science uses many programming languages"
    doc3 = "Python makes programming fun and efficient"
    
    id1 = engine.add_document(doc1)
    id2 = engine.add_document(doc2)
    id3 = engine.add_document(doc3)
    
    # Test search functionality
    results = engine.search("python programming")
    
    # Verify results
    assert len(results) > 0
    # First result should be doc1 or doc3 as they mention both terms
    assert results[0][0] in {id1, id3}
    # doc2 should have lower relevance as it only mentions "programming"
    assert any(r[0] == id2 and r[1] < results[0][1] for r in results)

def test_route_planner():
    """Test route planning functionality"""
    planner = RoutePlanner()
    
    # Add test locations
    planner.add_location("A", "Location A", 0.0, 0.0)
    planner.add_location("B", "Location B", 1.0, 1.0)
    planner.add_location("C", "Location C", 2.0, 2.0)
    
    # Add routes
    planner.add_route("A", "B", 10.0)
    planner.add_route("B", "C", 10.0)
    planner.add_route("A", "C", 25.0)  # Longer direct route
    
    # Test path finding
    path, distance = planner.find_shortest_path("A", "C")
    
    # Verify results
    assert path == ["A", "B", "C"]  # Should take shorter path through B
    assert distance == 20.0  # Total distance should be A->B + B->C
    
    # Test distance calculation
    loc_a = planner.locations["A"]
    loc_b = planner.locations["B"]
    calculated_distance = loc_a.distance_to(loc_b)
    assert calculated_distance > 0

def test_data_stream_analyzer():
    """Test data stream analysis functionality"""
    window = timedelta(minutes=5)
    analyzer = DataStreamAnalyzer(window)
    
    # Add test data
    base_time = datetime.now()
    test_data = [
        (base_time - timedelta(minutes=4, seconds=i), float(i))
        for i in range(10)
    ]
    
    for timestamp, value in test_data:
        analyzer.add_value(value, timestamp)
    
    # Test moving average
    avg = analyzer.get_moving_average()
    assert 4.0 <= avg <= 5.0  # Should be around 4.5
    
    # Test percentile calculation
    p95 = analyzer.get_percentile(0.95)
    assert 8.0 <= p95 <= 9.0  # Should be near the highest values
    
    # Test window expiration
    old_time = base_time - timedelta(minutes=10)
    analyzer.add_value(100.0, old_time)  # Should be ignored due to window
    assert abs(analyzer.get_moving_average() - avg) < 0.001  # Should not change

def test_text_search_edge_cases():
    """Test edge cases in text search"""
    engine = TextSearchEngine()
    
    # Test empty document
    id1 = engine.add_document("")
    results = engine.search("test")
    assert not any(r[0] == id1 for r in results)
    
    # Test search with no matches
    id2 = engine.add_document("This is a test document")
    results = engine.search("nonexistent")
    assert len(results) == 0
    
    # Test case insensitivity
    results = engine.search("TEST")
    assert len(results) == 1
    assert results[0][0] == id2

def test_route_planner_edge_cases():
    """Test edge cases in route planning"""
    planner = RoutePlanner()
    
    # Test isolated location
    planner.add_location("A", "Location A", 0.0, 0.0)
    planner.add_location("B", "Location B", 1.0, 1.0)
    
    # No route between locations
    with pytest.raises(KeyError):
        planner.find_shortest_path("A", "B")
    
    # Test same start and end
    planner.add_route("A", "A", 0.0)
    path, distance = planner.find_shortest_path("A", "A")
    assert path == ["A"]
    assert distance == 0.0

def test_data_stream_analyzer_edge_cases():
    """Test edge cases in data stream analysis"""
    analyzer = DataStreamAnalyzer(timedelta(minutes=5))
    
    # Test empty stream
    assert analyzer.get_moving_average() == 0
    assert analyzer.get_percentile(0.95) == 0
    
    # Test single value
    analyzer.add_value(10.0)
    assert analyzer.get_moving_average() == 10.0
    assert analyzer.get_percentile(0.5) == 10.0
    
    # Test window expiration with single value
    analyzer.add_value(20.0, datetime.now() - timedelta(minutes=10))
    assert analyzer.get_moving_average() == 0  # Value should expire