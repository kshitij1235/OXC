def open_file(file_name):
    try:
        with open(file_name, 'r') as file:
            contents = file.read()
            print("File contents:\n", contents)
    except FileNotFoundError:
        print("Error: File not found.")

file_name = 'nonexistent.txt'
open_file(file_name)
