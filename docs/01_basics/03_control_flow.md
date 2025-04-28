# Python Control Flow

## Conditional Statements

### If Statement
```python
age = 18

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")

# One-line conditional (ternary operator)
status = "adult" if age >= 18 else "minor"
```

### Match Statement (Python 3.10+)
```python
status = 404

match status:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case _:
        print("Unknown status")

# Match with patterns
command = ["ls", "-l"]
match command:
    case ["ls"]:
        print("List directory")
    case ["ls", *flags]:
        print(f"List directory with flags: {flags}")
    case ["cd", path]:
        print(f"Change to {path}")
    case _:
        print("Unknown command")
```

## Loops

### For Loop
```python
# Iterating over a sequence
for i in range(5):
    print(i)  # 0, 1, 2, 3, 4

# Iterating with enumerate
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")

# For with dictionary
person = {"name": "John", "age": 30}
for key, value in person.items():
    print(f"{key}: {value}")

# List comprehension
squares = [x**2 for x in range(10)]
```

### While Loop
```python
# Basic while loop
count = 0
while count < 5:
    print(count)
    count += 1

# While with else
attempts = 3
while attempts > 0:
    attempts -= 1
    if success():
        break
else:
    print("All attempts failed")
```

## Loop Control

### Break Statement
```python
# Exit loop early
for i in range(10):
    if i == 5:
        break
    print(i)  # Prints 0-4
```

### Continue Statement
```python
# Skip current iteration
for i in range(5):
    if i == 2:
        continue
    print(i)  # Prints 0,1,3,4
```

### Else Clause
```python
# Executes when loop completes normally
for i in range(5):
    if i == 10:
        break
    print(i)
else:
    print("Loop completed")  # This will print

# With break
for i in range(5):
    if i == 3:
        break
    print(i)
else:
    print("Loop completed")  # This won't print
```

## Exception Handling

### Try-Except
```python
try:
    num = int("invalid")
except ValueError as e:
    print(f"Conversion error: {e}")
except Exception as e:
    print(f"General error: {e}")
else:
    print("No exceptions occurred")
finally:
    print("This always executes")
```

### Context Managers (with)
```python
# File handling with automatic cleanup
with open("file.txt", "r") as file:
    content = file.read()

# Multiple context managers
with open("input.txt") as in_file, open("output.txt", "w") as out_file:
    out_file.write(in_file.read().upper())
```

## Best Practices

1. Use `elif` instead of nested `if` statements when possible
2. Prefer `for` loops over `while` loops when the number of iterations is known
3. Use list comprehensions for simple transformations
4. Always include specific exception types in try-except blocks
5. Use context managers for resource management

```python
# Good
if condition1:
    action1()
elif condition2:
    action2()
else:
    default_action()

# Avoid
if condition1:
    action1()
else:
    if condition2:
        action2()
    else:
        default_action()
```

## Common Patterns

### Switch/Case Alternative (Pre-Python 3.10)
```python
def switch_case(value):
    return {
        "a": "Alpha",
        "b": "Beta",
        "c": "Charlie"
    }.get(value, "Unknown")
```

### Guard Clause
```python
def process_user(user):
    if not user:
        return None
    if not user.is_active:
        return None
    return user.process()
```

### Loop with Counter
```python
from itertools import count

for i in count(1):
    if i > 10:
        break
    print(i)
```

## Exercises

1. Create a FizzBuzz implementation using if/elif/else
2. Write a password validation function using multiple conditions
3. Implement a number guessing game using while loops
4. Create a file processor using try-except and context managers
5. Write a function to validate input using guard clauses

## Advanced Examples

### State Machine
```python
def state_machine():
    state = "START"
    while True:
        match state:
            case "START":
                state = "RUNNING"
            case "RUNNING":
                state = "STOP"
            case "STOP":
                return
```

### Event Loop
```python
def simple_event_loop(events):
    while events:
        event = events.pop(0)
        match event["type"]:
            case "message":
                process_message(event)
            case "error":
                handle_error(event)
            case "shutdown":
                return
```

### Complex Iteration
```python
def process_nested_data(data):
    if isinstance(data, dict):
        return {k: process_nested_data(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [process_nested_data(item) for item in data]
    else:
        return data
```