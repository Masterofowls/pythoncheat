# Python List Methods and Functions Demonstration

# Creating a list
fruits = ['apple', 'banana', 'orange', 'grape']
numbers = [1, 5, 2, 8, 3]
print("Original lists:", fruits, numbers)

# 1. Adding elements
fruits.append('mango')        # Add at end
fruits.insert(1, 'kiwi')     # Insert at specific position
fruits.extend(['pear', 'plum'])  # Add multiple items
print("After adding elements:", fruits)

# 2. Removing elements
fruits.remove('banana')       # Remove specific item
popped = fruits.pop()        # Remove and return last item
popped_index = fruits.pop(1) # Remove and return item at index
print("After removing elements:", fruits)
print("Popped items:", popped, popped_index)
fruits.clear()               # Remove all items
print("After clearing:", fruits)

# 3. List information
numbers_length = len(numbers)           # Length of list
count_of_2 = numbers.count(2)          # Count occurrences
index_of_5 = numbers.index(5)          # Find index of item
print("List info - Length:", numbers_length, "Count of 2:", count_of_2, "Index of 5:", index_of_5)

# 4. Ordering
numbers.sort()               # Sort in ascending order
print("After sorting:", numbers)
numbers.reverse()            # Reverse the list
print("After reversing:", numbers)
numbers.sort(reverse=True)   # Sort in descending order
print("After descending sort:", numbers)

# 5. List operations
combined = fruits + numbers  # Concatenation
doubled = numbers * 2        # Repetition
sliced = numbers[1:4]       # Slicing
print("Combined:", combined)
print("Doubled:", doubled)
print("Sliced:", sliced)

# 6. Built-in functions for lists
maximum = max(numbers)       # Maximum value
minimum = min(numbers)       # Minimum value
total = sum(numbers)        # Sum of numbers
sorted_new = sorted(numbers) # Return new sorted list
print("Stats - Max:", maximum, "Min:", minimum, "Sum:", total)
print("New sorted list:", sorted_new)

# 7. Membership testing
contains_apple = 'apple' in fruits      # Check if item exists
print("Contains apple?", contains_apple)

# 8. List comprehension
squares = [x**2 for x in numbers]       # Create new list with squares
print("Squares:", squares)