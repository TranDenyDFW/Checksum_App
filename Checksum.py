import hashlib
import os

# Function to create a checksum for a file or folder
def create_checksum(path):
    if os.path.exists(path):
        if os.path.isdir(path):
            # If the path is a folder, get all the files within the folder
            file_list = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        else:
            # If the path is a file, use it directly
            file_list = [path]

        # Calculate the checksum for each file in the list
        checksums = []
        for file in file_list:
            hasher = hashlib.sha256()
            with open(file, 'rb') as f:
                while True:
                    data = f.read(65536)
                    if not data:
                        break
                    hasher.update(data)
            checksum = f"{hasher.hexdigest()}  {file}"
            checksums.append(checksum)

        return checksums
    else:
        print(f"File or folder not found: {path}. Checking the current directory.")
        current_directory = os.getcwd()
        return create_checksum(current_directory)

# Function to check checksums against a file or folder
def check_checksum(path, checksum_file):
    if os.path.exists(path):
        if os.path.isdir(path):
            # If the path is a folder, get all the files within the folder
            file_list = [os.path.join(path, file) for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
        else:
            # If the path is a file, use it directly
            file_list = [path]

        # Read the stored checksums from the checksum file
        with open(checksum_file, 'r') as f:
            stored_checksums = f.read().splitlines()

        # Calculate the checksum for each file and compare it with the stored checksum
        for file in file_list:
            hasher = hashlib.sha256()
            with open(file, 'rb') as f:
                while True:
                    data = f.read(65536)  # Read the file in 64k chunks
                    if not data:
                        break
                    hasher.update(data)
            current_checksum = f"{hasher.hexdigest()}  {file}"

            if current_checksum in stored_checksums:
                print(f"Checksum for {file} matches the stored checksum.")
            else:
                print(f"Checksum for {file} does not match the stored checksum.")
    else:
        print(f"File or folder not found: {path}. Checking the current directory.")
        current_directory = os.getcwd()
        check_checksum(current_directory, checksum_file)

# Prompt the user to choose an operation
while True:
    print("Choose an operation:")
    print("1. Create Checksum")
    print("2. Check Checksum")
    print("3. Exit")
    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        path = input("Enter the path to the file or folder for checksum calculation: ")
        checksums = create_checksum(path)
        txtfile = path.split('.')[0] + '_checksum.txt'
        with open(txtfile, 'w') as output_file:
            output_file.write('\n'.join(checksums))
        print("Checksums created.")
    elif choice == '2':
        path = input("Enter the path to the file or folder for checksum comparison: ")
        checksum_file = path.split('.')[0] + '_checksum.txt'
        if not os.path.isfile(checksum_file):
            checksum_file = input("Enter the path to the checksum file: ")
        check_checksum(path, checksum_file)
    elif choice == '3':
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
