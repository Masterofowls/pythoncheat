# Example demonstrating different types of methods in Python

class ExampleClass:
    # Class variable
    class_variable = "I'm a class variable"
    
    def __init__(self, value):
        # Instance variable
        self.value = value
    
    # Regular instance method
    def instance_method(self):
        return f"Instance method with value: {self.value}"
    
    # Class method (can access class state)
    @classmethod
    def class_method(cls):
        return f"Class method accessing {cls.class_variable}"
    
    # Static method (can't access instance or class state)
    @staticmethod
    def static_method():
        return "Static method"
    
    # Property decorator (getter)
    @property
    def getter_example(self):
        return self.value
    
    # Setter decorator
    @getter_example.setter
    def getter_example(self, new_value):
        self.value = new_value

# Example usage
if __name__ == "__main__":
    # Create instance
    obj = ExampleClass("test")
    
    # Call instance method
    print(obj.instance_method())
    
    # Call class method
    print(ExampleClass.class_method())
    
    # Call static method
    print(ExampleClass.static_method())
    
    # Use property
    print(obj.getter_example)
    obj.getter_example = "new value"