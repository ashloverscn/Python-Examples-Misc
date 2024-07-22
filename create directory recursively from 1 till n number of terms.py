import os

max_directory = 8

def create_directories(n):
    # Loop from 1 to n (inclusive)
    for i in range(1, n + 1):
        # Create directory with name as the number
        directory_name = str(i)
        os.makedirs(directory_name, exist_ok=True)
        print(f"Directory '{directory_name}' created.")

create_directories(max_directory)

