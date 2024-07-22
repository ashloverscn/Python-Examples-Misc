import os
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

print(f'All invalid email-address and that is not an email-address have been removed from {data_xlsx_file}.')

# Write data to data xlsx file
#df.to_excel(data_xlsx_file, index=False)

#print(f'Data successfully written back to {data_xlsx_file}.')

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
#csv_file = 'contacts.csv'
#df.to_csv(csv_file, index=False)

# Write data to XLSX file
#xlsx_file = 'contacts.xlsx'
#df.to_excel(xlsx_file, index=False)

#print(f'Data successfully written to {csv_file}.')
#print(f'Data successfully written to {xlsx_file}.')

# Write formated data back to XLSX file
df.to_excel(data_xlsx_file, index=False)
print(f'Data successfully formated and written back to {data_xlsx_file}.')

config_data_file = 'Split-O-Splice.config'

def read_config_file(filename):
    config = {}
    with open(filename, 'r') as f:
        for line in f:
            # Ignore comments and empty lines
            if line.strip() and not line.strip().startswith('#'):
                key, value = line.strip().split('=')
                config[key.strip()] = value.strip()
    return config

# Reading variables from the config dictionary
config = read_config_file(config_data_file)
max_directory = config.get('max_directory') # data-division or interger-number
chunk_size = int(config.get('chunk_size')) # interger-number
chunk_stamp = config.get('chunk_stamp') # colour-yellow or delete-rows-on-finish
test_interval = int(config.get('test_interval')) # interger-number

# Count the number of valid data rows (assuming any non-null row is valid)
data_rows_valid = df.dropna().shape[0]
# Calculate max_directory based on valid data rows
if max_directory  == "data-division":
    if data_rows_valid > 0:
        max_directory = data_rows_valid // chunk_size
        if data_rows_valid % chunk_size != 0:
            max_directory = max_directory + 1
        
# Printing out the variables
print("valid_data_rows:", data_rows_valid)
print("max_directory:", max_directory)
print("chunk_size:", chunk_size)
print("chunk_stamp:", chunk_stamp)
print("test_interval:", test_interval)

def create_directories(n):
    # Loop from 1 to n (inclusive)
    for i in range(1, n + 1):
        # Create directory with name as the number
        directory_name = str(i)
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' created.")

create_directories(max_directory)

input("Press any Key to Exit")
