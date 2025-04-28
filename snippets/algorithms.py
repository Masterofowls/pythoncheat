"""
Common algorithm implementations in Python.
Includes searching, sorting, and graph algorithms with practical examples.
"""
from typing import TypeVar, List, Dict, Set, Optional, Tuple
from collections import deque, defaultdict
import heapq
import time
from functools import wraps

T = TypeVar('T')
Number = TypeVar('Number', int, float)

def measure_time(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} took {end - start:.6f} seconds")
        return result
    return wrapper

class Searching:
    """Common searching algorithms"""
    
    @staticmethod
    def binary_search(arr: List[Number], target: Number) -> Optional[int]:
        """Binary search implementation
        Returns index of target or None if not found"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        return None
    
    @staticmethod
    def binary_search_rightmost(arr: List[Number], target: Number) -> int:
        """Find rightmost position to insert target"""
        left, right = 0, len(arr)
        
        while left < right:
            mid = (left + right) // 2
            if arr[mid] > target:
                right = mid
            else:
                left = mid + 1
        return left
    
    @staticmethod
    def find_peak(arr: List[Number]) -> int:
        """Find a peak element in array
        Returns index of any peak element"""
        left, right = 0, len(arr) - 1
        
        while left < right:
            mid = (left + right) // 2
            if arr[mid] > arr[mid + 1]:
                right = mid
            else:
                left = mid + 1
        return left

class Sorting:
    """Common sorting algorithms"""
    
    @staticmethod
    @measure_time
    def quicksort(arr: List[T]) -> List[T]:
        """Quicksort implementation"""
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return Sorting.quicksort(left) + middle + Sorting.quicksort(right)
    
    @staticmethod
    @measure_time
    def mergesort(arr: List[T]) -> List[T]:
        """Mergesort implementation"""
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = Sorting.mergesort(arr[:mid])
        right = Sorting.mergesort(arr[mid:])
        
        return Sorting._merge(left, right)
    
    @staticmethod
    def _merge(left: List[T], right: List[T]) -> List[T]:
        """Helper method for mergesort"""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class GraphAlgorithms:
    """Common graph algorithms"""
    
    @staticmethod
    def dijkstra(graph: Dict[str, Dict[str, int]], start: str) -> Dict[str, int]:
        """Dijkstra's shortest path algorithm
        Returns dictionary of shortest distances from start"""
        distances = {node: float('infinity') for node in graph}
        distances[start] = 0
        pq = [(0, start)]
        visited = set()
        
        while pq:
            current_distance, current_node = heapq.heappop(pq)
            
            if current_node in visited:
                continue
            
            visited.add(current_node)
            
            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight
                
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))
        
        return distances
    
    @staticmethod
    def bfs(graph: Dict[str, List[str]], start: str) -> List[str]:
        """Breadth-first search implementation"""
        visited = set()
        queue = deque([start])
        result = []
        
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                result.append(node)
                queue.extend(n for n in graph[node] if n not in visited)
        
        return result
    
    @staticmethod
    def dfs(graph: Dict[str, List[str]], start: str) -> List[str]:
        """Depth-first search implementation"""
        visited = set()
        result = []
        
        def dfs_recursive(node: str) -> None:
            visited.add(node)
            result.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs_recursive(neighbor)
        
        dfs_recursive(start)
        return result

class DynamicProgramming:
    """Common dynamic programming problems"""
    
    @staticmethod
    def longest_common_subsequence(s1: str, s2: str) -> str:
        """Find longest common subsequence of two strings"""
        dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
        
        for i in range(1, len(s1) + 1):
            for j in range(1, len(s2) + 1):
                if s1[i-1] == s2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Reconstruct the sequence
        result = []
        i, j = len(s1), len(s2)
        while i > 0 and j > 0:
            if s1[i-1] == s2[j-1]:
                result.append(s1[i-1])
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        return ''.join(reversed(result))
    
    @staticmethod
    def knapsack(values: List[int], weights: List[int], capacity: int) -> int:
        """0/1 Knapsack problem solution"""
        n = len(values)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i-1] <= w:
                    dp[i][w] = max(
                        values[i-1] + dp[i-1][w-weights[i-1]],
                        dp[i-1][w]
                    )
                else:
                    dp[i][w] = dp[i-1][w]
        
        return dp[n][capacity]

def demonstrate_algorithms() -> None:
    """Demonstrate usage of algorithm implementations"""
    # Searching
    arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(f"Binary search for 5: {Searching.binary_search(arr, 5)}")
    print(f"Find peak in [1,3,5,2,1]: {Searching.find_peak([1,3,5,2,1])}")
    
    # Sorting
    unsorted = [64, 34, 25, 12, 22, 11, 90]
    print("Quicksort:", Sorting.quicksort(unsorted.copy()))
    print("Mergesort:", Sorting.mergesort(unsorted.copy()))
    
    # Graph algorithms
    graph = {
        'A': {'B': 4, 'C': 2},
        'B': {'A': 4, 'C': 1, 'D': 5},
        'C': {'A': 2, 'B': 1, 'D': 8},
        'D': {'B': 5, 'C': 8}
    }
    print(f"Dijkstra from A: {GraphAlgorithms.dijkstra(graph, 'A')}")
    
    # Dynamic Programming
    s1, s2 = "ABCDGH", "AEDFHR"
    print(f"LCS of {s1} and {s2}: {DynamicProgramming.longest_common_subsequence(s1, s2)}")
    
    values = [60, 100, 120]
    weights = [10, 20, 30]
    capacity = 50
    print(f"Knapsack solution: {DynamicProgramming.knapsack(values, weights, capacity)}")

if __name__ == '__main__':
    demonstrate_algorithms()