from functools import reduce

# Basic lambda function examples
add = lambda x, y: x + y
square = lambda x: x ** 2
is_even = lambda x: x % 2 == 0

# Lambda with built-in functions
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
evens = list(filter(lambda x: x % 2 == 0, numbers))
doubles = list(map(lambda x: x * 2, numbers))
sum_pairs = list(map(lambda x, y: x + y, [1, 2, 3], [4, 5, 6]))

# Lambda in sorting
points = [(1, 2), (3, 1), (0, 4), (2, 3)]
sorted_by_y = sorted(points, key=lambda point: point[1])

# Lambda in reduce
product = reduce(lambda x, y: x * y, numbers)

def main():
    # Test basic lambda functions
    print(f"Add: {add(5, 3)}")  # 8
    print(f"Square: {square(4)}")  # 16
    print(f"Is 5 even? {is_even(5)}")  # False
    
    # Test filter and map
    print(f"Even numbers: {evens}")  # [2, 4, 6, 8]
    print(f"Doubled numbers: {doubles}")  # [2, 4, 6, 8, 10, 12, 14, 16, 18]
    print(f"Sum pairs: {sum_pairs}")  # [5, 7, 9]
    
    # Test sorting
    print(f"Sorted by y-coordinate: {sorted_by_y}")  # [(3, 1), (1, 2), (2, 3), (0, 4)]
    
    # Test reduce
    print(f"Product of all numbers: {product}")  # 362880

if __name__ == "__main__":
    main()