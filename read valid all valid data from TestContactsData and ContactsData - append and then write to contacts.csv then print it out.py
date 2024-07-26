import pandas as pd

# Read test data from Excel file
test_contacts_data_xlsx_file = 'TestContactsData.xlsx'
TestContactsData = pd.read_excel(test_contacts_data_xlsx_file, usecols=['name', 'email', 'repeat', 'sent'])
# Read contacts data from Excel file
contacts_data_xlsx_file = 'ContactsData.xlsx'
ContactsData = pd.read_excel(contacts_data_xlsx_file, usecols=['name', 'email', 'repeat', 'sent'])
# fill NaN values with empty String
TestContactsData.fillna('', inplace=True)
ContactsData.fillna('', inplace=True)
# Find the number of valid rows in both 
test_contacts_data_rows_valid = TestContactsData.dropna().shape[0]
contacts_data_rows_valid = ContactsData.dropna().shape[0]
# Printing out the number of rows in both 
print("valid_test_contacts_data_rows:", test_contacts_data_rows_valid)
print("valid_contacts_data_rows:", contacts_data_rows_valid)
#print(TestContactsData)
#print(ContactsData)

max_directory = 8
chunk_size = 18
test_interval = 100
next_data = chunk_size

# Create an empty ContactsDataFrame
ContactsDataFrame = pd.DataFrame()
# Append TestContactsData to ContactsDataFrame
ContactsDataFrame = pd.concat([ContactsDataFrame, TestContactsData], ignore_index=True)
# Append first 250 rows to ContactsDataFrame
ContactsDataFrame = pd.concat([ContactsDataFrame, ContactsData.head(chunk_size)], ignore_index=True)

# Write ContactsDataFrame to a CSV file
ContactsDataFrame.to_csv('contacts.csv', index=False, na_rep='')
# Print confirmation
print("ContactsDataFrame has been written to 'contacts.csv'")
# Print the DataFrame
print(ContactsDataFrame)

# Open and read the UTF-8 encoded contacts.csv text file
with open('contacts.csv', 'r', encoding='utf-8') as contacts_csv:
    # Read the file contents
    contacts = contacts_csv.read()
# Print the file contents
print(contacts)
