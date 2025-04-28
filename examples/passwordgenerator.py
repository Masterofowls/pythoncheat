import random
import string

def generate_password(length=12, use_uppercase=True, use_numbers=True, use_special=True):
    """
    Generate a secure password with customizable options
    """
    # Define character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase if use_uppercase else ''
    numbers = string.digits if use_numbers else ''
    special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?' if use_special else ''
    
    # Combine all allowed characters
    all_chars = lowercase + uppercase + numbers + special_chars
    
    # Ensure at least one character from each selected type
    password = []
    password.append(random.choice(lowercase))
    if use_uppercase:
        password.append(random.choice(uppercase))
    if use_numbers:
        password.append(random.choice(numbers))
    if use_special:
        password.append(random.choice(special_chars))
        
    # Fill the rest of the password length
    while len(password) < length:
        password.append(random.choice(all_chars))
    
    # Shuffle the password
    random.shuffle(password)
    
    return ''.join(password)

if __name__ == "__main__":
    # Example usage
    password = generate_password(length=16, use_uppercase=True, use_numbers=True, use_special=True)
    print(f"Generated password: {password}")