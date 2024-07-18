import pandas as pd
import re

# Read data from Excel file
data_xlsx_file = 'data.xlsx'
df = pd.read_excel(data_xlsx_file)

# Shift the rows down by one time
df = df.shift(periods=1)

# Insert the header "email" to the first column
df.columns = ['email'] + list(df.columns[1:])

# Remove rows with NaN values
df.dropna(inplace=True)

# Remove rows with invalid email addresses
def is_valid_email(email):
    if pd.isnull(email):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

df = df[df['email'].apply(is_valid_email)]

print(f'All invalid email-addresse and that is not an email-address have been removed from {data_xlsx_file}.')

# Write data to data xlsx file
data_xlsx_file = 'data.xlsx'
df.to_excel(data_xlsx_file, index=False)

print(f'Data successfully written back to {data_xlsx_file}.')

# Ensure "email" column is present
if 'email' not in df.columns:
    raise ValueError('"email" column is missing in the Excel file.')

# Ensure "name" column is present and fill with "Customer" if missing
if 'name' not in df.columns:
    df.insert(0, 'name', 'Customer')

# Add a new column "repeat" filled with 1 after the "email" column
df.insert(df.columns.get_loc('email') + 1, 'repeat', 1)

# Add an empty column "sent" after the "repeat" column
df.insert(df.columns.get_loc('repeat') + 1, 'sent', '')

# Write data to CSV file
csv_file = 'contacts.csv'
df.to_csv(csv_file, index=False)

# Write data to XLSX file
xlsx_file = 'contacts.xlsx'
df.to_excel(xlsx_file, index=False)

print(f'Data successfully written to {csv_file}.')
print(f'Data successfully written to {xlsx_file}.')
