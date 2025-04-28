# Python Operators

## Arithmetic Operators

```python
# Basic arithmetic
a = 10
b = 3

addition = a + b        # 13
subtraction = a - b     # 7
multiplication = a * b  # 30
division = a / b        # 3.3333... (float division)
floor_division = a // b # 3 (integer division)
modulus = a % b        # 1 (remainder)
exponent = a ** b      # 1000 (10 to the power of 3)

# Augmented assignment operators
x = 5
x += 3  # Same as: x = x + 3
x -= 2  # Same as: x = x - 2
x *= 4  # Same as: x = x * 4
x /= 2  # Same as: x = x / 2
x //= 3 # Same as: x = x // 3
x %= 2  # Same as: x = x % 2
x **= 2 # Same as: x = x ** 2
```

## Comparison Operators

```python
a = 10
b = 20

equal = a == b           # False
not_equal = a != b       # True
greater_than = a > b     # False
less_than = a < b        # True
greater_equal = a >= b   # False
less_equal = a <= b      # True

# Chained comparisons
x = 5
result = 1 < x < 10     # True
```

## Logical Operators

```python
# and - returns True if both statements are true
x = True and True    # True
y = True and False   # False

# or - returns True if at least one statement is true
x = True or False    # True
y = False or False   # False

# not - reverses the result
x = not True         # False
y = not False        # True

# Short-circuit evaluation
result = True or print("Never executed")  # Short-circuits at True
result = False and print("Never executed")  # Short-circuits at False
```

## Identity Operators

```python
# is - returns True if both variables are the same object
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a is b)     # False (different objects)
print(a is c)     # True (same object)
print(a is not b) # True
```

## Membership Operators

```python
# in - returns True if a value is found in the sequence
numbers = [1, 2, 3, 4, 5]
print(3 in numbers)      # True
print(6 in numbers)      # False
print(6 not in numbers)  # True

# Works with strings too
text = "Python"
print('y' in text)       # True
```

## Bitwise Operators

```python
a = 60      # 60 = 0011 1100 
b = 13      # 13 = 0000 1101

# & (AND)
print(a & b)   # 12 = 0000 1100

# | (OR)
print(a | b)   # 61 = 0011 1101

# ^ (XOR)
print(a ^ b)   # 49 = 0011 0001

# ~ (NOT)
print(~a)      # -61 = 1100 0011

# << (left shift)
print(a << 2)  # 240 = 1111 0000

# >> (right shift)
print(a >> 2)  # 15 = 0000 1111
```

## Operator Precedence

Order of operations (highest to lowest):
1. `**` (exponentiation)
2. `~`, `+`, `-` (unary operators)
3. `*`, `/`, `//`, `%` (multiplication, division)
4. `+`, `-` (addition, subtraction)
5. `<<`, `>>` (shifts)
6. `&` (bitwise AND)
7. `^` (bitwise XOR)
8. `|` (bitwise OR)
9. `==`, `!=`, `>`, `>=`, `<`, `<=`, `is`, `is not`, `in`, `not in` (comparisons)
10. `not`
11. `and`
12. `or`

```python
# Example of precedence
result = 2 + 3 * 4    # 14 (not 20)
result = (2 + 3) * 4  # 20 (using parentheses)
```

## Best Practices

1. Use parentheses for clarity even when not strictly needed
2. Avoid complex nested operations
3. Use augmented assignments when possible
4. Be careful with identity operators (`is`) vs equality operators (`==`)

## Common Pitfalls

```python
# 1. Float comparison
x = 0.1 + 0.2
print(x == 0.3)  # False! Due to floating-point precision
print(abs(x - 0.3) < 1e-9)  # Better way to compare floats

# 2. Chaining operators incorrectly
x = 5
print(1 <= x <= 10)  # Correct: checks if x is between 1 and 10
print(1 <= x and x <= 10)  # Same as above, but more verbose

# 3. Using 'is' for value comparison
a = 1000
b = 1000
print(a is b)  # False! Use == for value comparison
print(a == b)  # True
```

## Practice Examples

```python
# 1. Temperature conversion
celsius = 25
fahrenheit = (celsius * 9/5) + 32
print(f"{celsius}°C = {fahrenheit}°F")

# 2. Circle calculations
import math
radius = 5
area = math.pi * radius ** 2
circumference = 2 * math.pi * radius
print(f"Area: {area:.2f}, Circumference: {circumference:.2f}")

# 3. Bitwise operations for flags
READ = 0b100
WRITE = 0b010
EXECUTE = 0b001

permissions = READ | WRITE  # 0b110
can_read = permissions & READ == READ  # True
can_execute = permissions & EXECUTE == EXECUTE  # False
```

## Exercises

1. Create a BMI calculator using arithmetic operators
2. Implement a simple password checker using logical operators
3. Create a function that checks if a year is a leap year using comparison operators
4. Write a program that uses bitwise operators to pack multiple boolean flags into a single integer