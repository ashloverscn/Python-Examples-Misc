import pandas as pd

# Load the Excel file into a DataFrame
file_path = 'data.xlsx'
df = pd.read_excel(file_path)

# Count the number of valid data rows (assuming any non-null row is valid)
data_rows_valid = df.dropna().shape[0]

# Define chunk_size (changed to 300)
chunk_size = 300 

# Define max_directory (changed to 300)
max_directory  = "data-division"

# Calculate max_directory based on valid data rows
if max_directory  == "data-division":
    if data_rows_valid > 0:
        max_directory = data_rows_valid // chunk_size
        
# Display the results
print(f"Number of valid data rows: {data_rows_valid}")
print(f"max_directory: {max_directory}")
