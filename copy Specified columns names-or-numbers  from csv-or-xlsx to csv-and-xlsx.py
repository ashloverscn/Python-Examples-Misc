import pandas as pd

# Define the file paths
input_file_csv = 'ContactsData.csv'
input_file_xlsx = 'ContactsData.xlsx'
output_file_csv = 'contacts.csv'
output_file_xlsx = 'contacts.xlsx'

# Read the first 250 rows from specific columns
#Read csv input file using row header name
df = pd.read_csv(input_file_csv, usecols=['name', 'email', 'repeat', 'sent'], nrows=250)
#Read csv input file using row header number
df = pd.read_csv(input_file_csv, usecols=[0, 1, 2, 3], nrows=250)

# Read the first 250 rows from specific columns
#Read xlsx input file using row header name
df = pd.read_excel(input_file_xlsx, usecols=['name', 'email', 'repeat', 'sent'], nrows=250)
#Read xlsx input file using row header number
df = pd.read_excel(input_file_xlsx, usecols=[0, 1, 2, 3], nrows=250)

# Write to contacts1.csv
df.to_csv(output_file_csv, index=False, na_rep='')
# Write to contacts1.xlsx
df.to_excel(output_file_xlsx, index=False, na_rep='')
