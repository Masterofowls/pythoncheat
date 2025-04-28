"""
Advanced algorithm implementations with practical applications.
Demonstrates real-world usage of complex algorithms and optimization techniques.
"""
from typing import TypeVar, List, Dict, Set, Tuple, Optional, Any
from collections import defaultdict, Counter
from dataclasses import dataclass
import heapq
import time
from datetime import datetime, timedelta
import re
from functools import lru_cache

T = TypeVar('T')

class TextSearchEngine:
    """Practical implementation of text search algorithms"""
    
    def __init__(self):
        self.documents: Dict[int, str] = {}
        self.index: Dict[str, Set[int]] = defaultdict(set)
        self._doc_counter = 0
    
    def add_document(self, content: str) -> int:
        """Add document to search engine using inverted index"""
        doc_id = self._doc_counter
        self.documents[doc_id] = content
        
        # Create inverted index
        words = self._tokenize(content.lower())
        for word in words:
            self.index[word].add(doc_id)
        
        self._doc_counter += 1
        return doc_id
    
    def search(self, query: str, max_results: int = 10) -> List[Tuple[int, float]]:
        """Search documents using TF-IDF scoring"""
        query_terms = self._tokenize(query.lower())
        scores: Dict[int, float] = defaultdict(float)
        
        # Calculate TF-IDF scores
        for term in query_terms:
            if term in self.index:
                idf = self._calculate_idf(term)
                for doc_id in self.index[term]:
                    tf = self._calculate_tf(term, self.documents[doc_id])
                    scores[doc_id] += tf * idf
        
        # Return top N results
        return sorted(
            [(doc_id, score) for doc_id, score in scores.items()],
            key=lambda x: x[1],
            reverse=True
        )[:max_results]
    
    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Convert text into tokens"""
        return re.findall(r'\w+', text)
    
    def _calculate_tf(self, term: str, document: str) -> float:
        """Calculate term frequency"""
        words = self._tokenize(document.lower())
        return words.count(term) / len(words)
    
    def _calculate_idf(self, term: str) -> float:
        """Calculate inverse document frequency"""
        from math import log
        return log(len(self.documents) / len(self.index[term]))

class RoutePlanner:
    """Practical implementation of path finding algorithms"""
    
    @dataclass
    class Location:
        """Represents a location with coordinates and metadata"""
        id: str
        name: str
        lat: float
        lon: float
        
        def distance_to(self, other: 'RoutePlanner.Location') -> float:
            """Calculate distance between locations"""
            from math import radians, sin, cos, sqrt, atan2
            
            R = 6371  # Earth's radius in km
            
            lat1, lon1 = radians(self.lat), radians(self.lon)
            lat2, lon2 = radians(other.lat), radians(other.lon)
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            
            return R * c
    
    def __init__(self):
        self.locations: Dict[str, RoutePlanner.Location] = {}
        self.routes: Dict[str, Dict[str, float]] = defaultdict(dict)
    
    def add_location(self, id: str, name: str, lat: float, lon: float) -> None:
        """Add a location to the route network"""
        self.locations[id] = self.Location(id, name, lat, lon)
    
    def add_route(self, from_id: str, to_id: str, distance: Optional[float] = None) -> None:
        """Add a route between locations"""
        if distance is None:
            distance = self.locations[from_id].distance_to(self.locations[to_id])
        
        self.routes[from_id][to_id] = distance
        self.routes[to_id][from_id] = distance
    
    def find_shortest_path(self, start: str, end: str) -> Tuple[List[str], float]:
        """Find shortest path using Dijkstra's algorithm with path reconstruction"""
        distances = {loc: float('infinity') for loc in self.locations}
        distances[start] = 0
        previous: Dict[str, Optional[str]] = {loc: None for loc in self.locations}
        unvisited = set(self.locations.keys())
        
        while unvisited:
            # Find unvisited location with minimum distance
            current = min(unvisited, key=lambda x: distances[x])
            
            if current == end:
                break
            
            unvisited.remove(current)
            
            # Update distances to neighbors
            for neighbor, distance in self.routes[current].items():
                if neighbor in unvisited:
                    new_distance = distances[current] + distance
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        previous[neighbor] = current
        
        # Reconstruct path
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        
        return list(reversed(path)), distances[end]

class DataStreamAnalyzer:
    """Real-time data stream analysis algorithms"""
    
    def __init__(self, window_size: timedelta):
        self.window_size = window_size
        self.values: List[Tuple[datetime, float]] = []
        self._sum = 0
        self._count = 0
    
    def add_value(self, value: float, timestamp: Optional[datetime] = None) -> None:
        """Add a value to the stream"""
        if timestamp is None:
            timestamp = datetime.now()
        
        # Remove old values
        cutoff = timestamp - self.window_size
        while self.values and self.values[0][0] < cutoff:
            _, old_value = self.values.pop(0)
            self._sum -= old_value
            self._count -= 1
        
        # Add new value
        self.values.append((timestamp, value))
        self._sum += value
        self._count += 1
    
    def get_moving_average(self) -> float:
        """Calculate moving average over the window"""
        return self._sum / self._count if self._count > 0 else 0
    
    def get_percentile(self, percentile: float) -> float:
        """Calculate percentile of current values"""
        if not self.values:
            return 0
        
        sorted_values = sorted(v for _, v in self.values)
        k = (len(sorted_values) - 1) * percentile
        f = int(k)
        c = int(k + 1 if k < len(sorted_values) - 1 else k)
        d = k - f
        
        return sorted_values[f] * (1 - d) + sorted_values[c] * d

def demonstrate_algorithms():
    """Demonstrate usage of advanced algorithms"""
    # Text Search Example
    search_engine = TextSearchEngine()
    doc1_id = search_engine.add_document("Python is a great programming language")
    doc2_id = search_engine.add_document("Programming in Python is fun and productive")
    doc3_id = search_engine.add_document("Data structures and algorithms are fundamental")
    
    results = search_engine.search("python programming")
    print("\nSearch Results:")
    for doc_id, score in results:
        print(f"Document {doc_id}: {score:.4f}")
    
    # Route Planning Example
    planner = RoutePlanner()
    planner.add_location("NYC", "New York", 40.7128, -74.0060)
    planner.add_location("BOS", "Boston", 42.3601, -71.0589)
    planner.add_location("PHL", "Philadelphia", 39.9526, -75.1652)
    
    planner.add_route("NYC", "BOS")
    planner.add_route("NYC", "PHL")
    planner.add_route("BOS", "PHL")
    
    path, distance = planner.find_shortest_path("NYC", "PHL")
    print(f"\nShortest Path: {' -> '.join(path)}")
    print(f"Total Distance: {distance:.2f} km")
    
    # Data Stream Analysis Example
    analyzer = DataStreamAnalyzer(timedelta(minutes=5))
    for i in range(100):
        analyzer.add_value(i * 1.5, 
                         datetime.now() - timedelta(seconds=i))
    
    print(f"\nMoving Average: {analyzer.get_moving_average():.2f}")
    print(f"95th Percentile: {analyzer.get_percentile(0.95):.2f}")

if __name__ == '__main__':
    demonstrate_algorithms()