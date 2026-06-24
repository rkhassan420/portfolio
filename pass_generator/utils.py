import random
import string

def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character types selected.")

    password = ''.join(random.choices(characters, k=length))
    return password

def check_strength(password):
    score = 0

    # Criteria
    if len(password) >= 8:
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(c in string.punctuation for c in password):
        score += 1

    # Classification with colors
    if score <= 2:
        return {"strength": "Weak", "color": "red"}
    elif score <= 4:
        return {"strength": "Medium", "color": "orange"}
    else:  # score == 5
        return {"strength": "Strong", "color": "green"}
