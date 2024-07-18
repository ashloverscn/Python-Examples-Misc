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

# Load the Data Excel file Display the original DataFrame
data_xlsx = 'data.xlsx'

try:
    df = pd.read_excel(data_xlsx)
    print("Original DataFrame:")
    print(df)

except FileNotFoundError:
    print(f"Error: File '{data_xlsx}' not found.")
    exit(1)
except Exception as e:
    print(f"Error occurred while reading '{data_xlsx}': {str(e)}")
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

### Shift the rows down by one time
##shifted_df = df.shift(periods=1)
##
### Insert the header "email" to the first column
##shifted_df.columns = ['email'] + list(shifted_df.columns[1:])
##
### Remove rows with NaN values
##shifted_df.dropna(inplace=True)
##
### Remove rows with invalid email addresses
##def is_valid_email(email):
##    if pd.isnull(email):
##        return False
##    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
##    return bool(re.match(pattern, email))
##
##shifted_df = shifted_df[shifted_df['email'].apply(is_valid_email)]
##
### Write the cleaned DataFrame back to the original Excel file
##shifted_df.to_excel(data_xlsx, index=False)
##
