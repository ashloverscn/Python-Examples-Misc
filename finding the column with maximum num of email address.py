import pandas as pd
import re

# Function to count valid email addresses in a given text
def count_valid_emails(text):
    # Regular expression for matching email addresses
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    # Find all matches
    emails = re.findall(pattern, text)
    # Return the count of valid email addresses
    return len(emails)

# Load the Excel file
file_path = 'data.xlsx'

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print(f"Error: File '{file_path}' not found.")
    exit(1)
except Exception as e:
    print(f"Error occurred while reading '{file_path}': {str(e)}")
    exit(1)

# Initialize an empty list to store (column_name, max_valid_count) tuples
column_valid_counts = []

# Iterate through each column in the DataFrame
for column in df.columns:
    # Apply the count_valid_emails function to each element in the column
    valid_count = df[column].apply(lambda x: count_valid_emails(str(x))).sum()
    # Append (column_name, max_valid_count) tuple to the list
    column_valid_counts.append((column, valid_count))

# Find the column with the maximum number of valid email addresses
max_column = max(column_valid_counts, key=lambda x: x[1])

# Extract the row number (index) of the maximum count
max_row_index = column_valid_counts.index(max_column)

print(f"The row number '{max_row_index + 1}' has the maximum number of valid email addresses: {max_column[1]}")
