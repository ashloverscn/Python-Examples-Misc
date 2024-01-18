import re
import pandas as pd

def is_valid_email(email):
    #pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    pattern = r'^\s*[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\s*$'
    return re.match(pattern, email) is not None

# Example usage:
contactsData = pd.read_csv('contacts.csv')
for i in range(len(contactsData)):
    if is_valid_email(contactsData.at[int(i), 'email']):
        print("Valid email address")
    else:
        print("Invalid email address")
input()
