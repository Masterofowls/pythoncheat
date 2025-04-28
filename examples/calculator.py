class Calculator:
    def add(self, x, y):
        return x + y
    
    def subtract(self, x, y):
        return x - y
    
    def multiply(self, x, y):
        return x * y
    
    def divide(self, x, y):
        if y == 0:
            raise ValueError("Cannot divide by zero")
        return x / y
    
    def power(self, x, y):
        return x ** y
    
    def root(self, x, n):
        return x ** (1/n)

def main():
    calc = Calculator()
    
    while True:
        print("\nAdvanced Calculator")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Power")
        print("6. Root")
        print("7. Exit")
        
        try:
            choice = int(input("Enter choice (1-7): "))
            if choice == 7:
                print("Goodbye!")
                break
                
            if choice not in range(1, 7):
                print("Invalid choice!")
                continue
                
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == 1:
                print("Result:", calc.add(num1, num2))
            elif choice == 2:
                print("Result:", calc.subtract(num1, num2))
            elif choice == 3:
                print("Result:", calc.multiply(num1, num2))
            elif choice == 4:
                print("Result:", calc.divide(num1, num2))
            elif choice == 5:
                print("Result:", calc.power(num1, num2))
            elif choice == 6:
                print("Result:", calc.root(num1, num2))
                
        except ValueError as e:
            print("Error:", str(e))
        except Exception as e:
            print("An error occurred:", str(e))

if __name__ == "__main__":
    main()