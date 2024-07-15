import pandas as pd

# Step 1: Read the Excel file into a pandas DataFrame without header
data_xlsx = 'data.xlsx'
df = pd.read_excel(data_xlsx, header=None)

# Display the original DataFrame
print("Original DataFrame:")
print(df)

# Step 2: Shift the rows down by one time
shifted_df = df.shift(periods=1)

# Step 3: Write the shifted DataFrame back to the original Excel file
shifted_df.to_excel(data_xlsx, index=False, header=False)

print("\nShifted DataFrame saved back to:", data_xlsx)
