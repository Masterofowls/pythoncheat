import math
import numpy as np
from datetime import datetime, timedelta
from os import *
import json
import simplejson as json
import os
import json  # Standard JSON module
from json import loads, dumps  # Import specific JSON functions
from dotenv import load_dotenv  # requires python-dotenv package
from pathlib import Path

# Load environment variables from .env file
load_dotenv()
# Access environment variables
DATABASE_URL = os.getenv('DATABASE_URL')

# JSON usage examples
data_dict = {'key': 'value'}
json_string = json.dumps(data_dict)  # Convert dict to JSON string
parsed_data = json.loads(json_string)  # Parse JSON string to dict

# Import from other Python files
# Assuming you have these files in the same directory:
from my_module import my_function  # imports specific function
import my_package.sub_module  # imports whole module from package
from . import local_module  # relative import from same directory
from .utils import helper_function  # relative import from utils.py

# Rest of your existing code...
# Basic import

# Import with alias

# Import specific items from a module

# Import all items from a module (not recommended)

# Import with multiple lines
from collections import (
    defaultdict,
    Counter,
    deque
)

# Conditional import
try:
    import optional_package
except ImportError:
    optional_package = None

# Import from relative path
# Assuming this is in package/module.py
# from . import sibling_module
# from .. import parent_module
# from ..sibling import other_module

# Example of creating exportable items
__all__ = ['MyClass', 'my_function', 'CONSTANT']

# Variables that will be exported when using "from module import *"
CONSTANT = 100

# Class that can be imported
class MyClass:
    def __init__(self):
        self.value = 42

# Function that can be imported
def my_function():
    return "Hello, World!"

# Private function (by convention, not exported)
def _private_function():
    return "I'm private"

# Example of module level dunder names
if __name__ == '__main__':
    # This code only runs when the file is executed directly
    print("Running as main program")
    my_function()