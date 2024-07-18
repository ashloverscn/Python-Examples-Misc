import pandas as pd

# Define the file paths
input_file_csv = 'contacts.csv'
input_file_xlsx = 'contacts.xlsx'
output_file_csv = 'contacts1.csv'
output_file_xlsx = 'contacts1.xlsx'

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
df.to_csv(output_file_csv, index=False)
# Write to contacts1.xlsx
df.to_excel(output_file_xlsx, index=False)
