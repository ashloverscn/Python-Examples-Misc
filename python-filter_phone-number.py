import re

def extract_numbers_with_plus(input_string):
    numbers = ''.join(re.findall(r'\d+', input_string))
    return '+' + numbers

input_string = "The year i/>;97$3@1NhFdWs 2024, and the temperature is 30 degrees."
result = extract_numbers_with_plus(input_string)
print(result)
