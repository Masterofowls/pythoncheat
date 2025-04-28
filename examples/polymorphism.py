# Example of Polymorphism in Python

# 1. Method Overriding
class Animal:
    def speak(self):
        return "Some sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

# 2. Method Overloading (through default arguments)
class Calculator:
    def add(self, a, b=0, c=0):
        return a + b + c

# 3. Duck Typing
class Duck:
    def swim(self):
        return "Duck swimming"
    
    def fly(self):
        return "Duck flying"

class Swan:
    def swim(self):
        return "Swan swimming"
    
    def fly(self):
        return "Swan flying"

# 4. Operator Overloading
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"

# Example usage
def main():
    # Method Overriding
    print("\nMethod Overriding Example:")
    animals = [Animal(), Dog(), Cat()]
    for animal in animals:
        print(animal.speak())

    # Method Overloading
    print("\nMethod Overloading Example:")
    calc = Calculator()
    print(calc.add(1))          # 1
    print(calc.add(1, 2))       # 3
    print(calc.add(1, 2, 3))    # 6

    # Duck Typing
    print("\nDuck Typing Example:")
    def make_bird_swim(bird):
        print(bird.swim())

    duck = Duck()
    swan = Swan()
    make_bird_swim(duck)
    make_bird_swim(swan)

    # Operator Overloading
    print("\nOperator Overloading Example:")
    v1 = Vector(2, 3)
    v2 = Vector(3, 4)
    v3 = v1 + v2
    print(v3)

if __name__ == "__main__":
    main()