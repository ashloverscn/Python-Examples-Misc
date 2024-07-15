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

# Initialize an empty dictionary to store counts for each column
column_valid_counts = {}

# Iterate through each column in the DataFrame
for column in df.columns:
    # Apply the count_valid_emails function to each element in the column
    column_valid_counts[column] = df[column].apply(lambda x: count_valid_emails(str(x))).sum()

# Find the column with the maximum number of valid email addresses
max_column = max(column_valid_counts, key=column_valid_counts.get)
max_valid_count = column_valid_counts[max_column]

print(f"The column '{max_column}' has the maximum number of valid email addresses: {max_valid_count}")
