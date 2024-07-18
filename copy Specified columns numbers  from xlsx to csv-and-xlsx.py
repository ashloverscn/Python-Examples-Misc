import pandas as pd

# Define the file paths
input_file_xlsx = 'contacts.xlsx'
output_file_csv = 'contacts1.csv'
output_file_xlsx = 'contacts1.xlsx'

# Read the first 250 rows from columns 0 to 3 (0-based index) from Excel
df = pd.read_excel(input_file_xlsx, usecols=[0, 1, 2, 3], nrows=250)

# Write to contacts1.csv
df.to_csv(output_file_csv, index=False)
# Write to contacts1.xlsx
df.to_excel(output_file_xlsx, index=False)
