import pandas as pd

# Read data from Excel file
excel_file = 'data.xlsx'
df = pd.read_excel(excel_file)

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
