# Dictionary manipulation examples

def create_dict():
    """Create and return a sample dictionary"""
    return {'name': 'John', 'age': 30, 'city': 'New York'}

def add_or_update_item(dictionary, key, value):
    """Add new item or update existing item in dictionary"""
    dictionary[key] = value
    return dictionary

def remove_item(dictionary, key):
    """Remove item from dictionary if exists"""
    return dictionary.pop(key, None)

def clear_dict(dictionary):
    """Clear all items from dictionary"""
    dictionary.clear()
    return dictionary

def get_value(dictionary, key, default=None):
    """Get value from dictionary with optional default value"""
    return dictionary.get(key, default)

def merge_dicts(dict1, dict2):
    """Merge two dictionaries"""
    return dict1 | dict2  # Python 3.9+ syntax
    # return {**dict1, **dict2}  # Alternative for older Python versions

def get_keys(dictionary):
    """Get all keys from dictionary"""
    return list(dictionary.keys())

def get_values(dictionary):
    """Get all values from dictionary"""
    return list(dictionary.values())

def get_items(dictionary):
    """Get all key-value pairs from dictionary"""
    return list(dictionary.items())

def check_key_exists(dictionary, key):
    """Check if key exists in dictionary"""
    return key in dictionary

def copy_dict(dictionary):
    """Create a shallow copy of dictionary"""
    return dictionary.copy()

# Example usage
if __name__ == "__main__":
    # Create a new dictionary
    my_dict = create_dict()
    print("Original dictionary:", my_dict)

    # Add/update item
    my_dict = add_or_update_item(my_dict, 'email', 'john@example.com')
    print("After adding email:", my_dict)

    # Remove item
    removed_value = remove_item(my_dict, 'age')
    print("After removing age:", my_dict)

    # Get value with default
    phone = get_value(my_dict, 'phone', 'Not found')
    print("Phone number (with default):", phone)

    # Merge dictionaries
    dict2 = {'age': 31, 'country': 'USA'}
    merged = merge_dicts(my_dict, dict2)
    print("Merged dictionary:", merged)

    # Get keys, values, items
    print("Keys:", get_keys(merged))
    print("Values:", get_values(merged))
    print("Items:", get_items(merged))

    # Check if key exists
    print("Has 'name'?:", check_key_exists(merged, 'name'))

    # Clear dictionary
    cleared_dict = clear_dict(merged)
    print("Cleared dictionary:", cleared_dict)