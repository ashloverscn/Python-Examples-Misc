import pandas as pd
import re

# Read the Excel file into a pandas DataFrame without header
data_xlsx = 'data.xlsx'
df = pd.read_excel(data_xlsx, header=None)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Shift the rows down by one time
shifted_df = df.shift(periods=1)

# Insert the header "email" to the first column
shifted_df.columns = ['email'] + list(shifted_df.columns[1:])

# Remove rows with NaN values
shifted_df.dropna(inplace=True)

# Remove rows with invalid email addresses
def is_valid_email(email):
    if pd.isnull(email):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

shifted_df = shifted_df[shifted_df['email'].apply(is_valid_email)]

# Write the cleaned DataFrame back to the original Excel file
shifted_df.to_excel(data_xlsx, index=False)

print("\nShifted DataFrame with 'email' header, NaN rows, and invalid email addresses removed saved back to:", data_xlsx)
