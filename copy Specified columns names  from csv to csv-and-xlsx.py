import pandas as pd

# Define the file paths
input_file_csv = 'contacts.csv'
output_file_csv = 'contacts1.csv'
output_file_xlsx = 'contacts1.xlsx'

# Read the first 250 rows from specific columns
df = pd.read_csv(input_file_csv, usecols=['name', 'email', 'repeat', 'sent'], nrows=250)

# Write to contacts1.csv
df.to_csv(output_file_csv, index=False)
# Write to contacts1.xlsx
df.to_excel(output_file_xlsx, index=False)
