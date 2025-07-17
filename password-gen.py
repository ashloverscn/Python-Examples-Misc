import random

# Full set of printable US keyboard characters (excluding whitespace)
characters = (
    'abcdefghijklmnopqrstuvwxyz'
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    '0123456789'
    '~!@#$%^&*()_+`-={}|[]\\:";\'<>?,./'
)

# Ask user for number of characters
user_input = input("Enter the number of characters to scramble (default is 8): ").strip()

# Default to 8 if no valid number is provided
try:
    num_chars = int(user_input)
    if num_chars <= 0:
        raise ValueError
except ValueError:
    num_chars = 8

# Randomly select without replacement if possible
if num_chars <= len(characters):
    scrambled = ''.join(random.sample(characters, num_chars))
else:
    scrambled = ''.join(random.choices(characters, k=num_chars))  # allow duplicates if needed

# Append to file
with open('password.txt', 'a') as file:
    file.write(scrambled + '\n')

print(f"Scrambled string ({num_chars} chars) written to password.txt")
