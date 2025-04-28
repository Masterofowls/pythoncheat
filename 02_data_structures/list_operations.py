"""
Advanced List Operations and Best Practices in Python
"""

def list_comprehension_examples():
    # Basic list comprehension
    numbers = [1, 2, 3, 4, 5]
    squares = [x**2 for x in numbers]
    
    # List comprehension with condition
    even_squares = [x**2 for x in numbers if x % 2 == 0]
    
    # Nested list comprehension
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    flattened = [num for row in matrix for num in row]
    
    return squares, even_squares, flattened

def list_slicing_examples():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    
    # Basic slicing
    first_three = letters[:3]  # ['a', 'b', 'c']
    last_three = letters[-3:]  # ['e', 'f', 'g']
    
    # Slicing with step
    every_second = letters[::2]  # ['a', 'c', 'e', 'g']
    
    # Reverse list
    reversed_list = letters[::-1]  # ['g', 'f', 'e', 'd', 'c', 'b', 'a']
    
    return first_three, last_three, every_second, reversed_list

def list_methods_showcase():
    fruits = ['apple', 'banana', 'orange']
    
    # Adding elements
    fruits.append('grape')  # Add to end
    fruits.insert(1, 'mango')  # Insert at specific position
    fruits.extend(['kiwi', 'pear'])  # Add multiple items
    
    # Removing elements
    fruits.remove('banana')  # Remove by value
    last_fruit = fruits.pop()  # Remove and return last item
    del fruits[0]  # Remove by index
    
    # Other operations
    fruits.sort(reverse=True)  # Sort in descending order
    fruits_count = len(fruits)  # Get length
    mango_index = fruits.index('mango')  # Find index of item
    
    return fruits

def list_performance_tips():
    """
    Performance tips for working with lists:
    1. Use list comprehension instead of loops when creating lists
    2. Use extend() instead of multiple append() calls
    3. Use join() for string concatenation
    4. Use slice assignment for bulk operations
    """
    # Bad: Multiple append calls
    numbers = []
    for i in range(1000):
        numbers.append(i)
    
    # Good: List comprehension
    numbers = [i for i in range(1000)]
    
    # Bad: String concatenation in loop
    strings = ['a', 'b', 'c', 'd']
    result = ''
    for s in strings:
        result += s
    
    # Good: Using join
    result = ''.join(strings)
    
    return numbers, result

if __name__ == '__main__':
    # Example usage
    print("List Comprehension Examples:", list_comprehension_examples())
    print("List Slicing Examples:", list_slicing_examples())
    print("List Methods Example:", list_methods_showcase())
    print("Performance Examples:", list_performance_tips())