import os
import json
import hashlib

HASH_FILE = "hash_table.json"

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def traverse_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)
            hashes[path] = hash_file(path)
    return hashes

def generate_table(directory):
    hashes = traverse_directory(directory)
    with open(HASH_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)
    print("Hash table generated.")

def validate_hash(directory):
    if not os.path.exists(HASH_FILE):
        print("No hash table found.")
        return
    
    with open(HASH_FILE) as f:
        stored = json.load(f)

    current = traverse_directory(directory)

    for path, h in stored.items():
        if path not in current:
            print(f"{path} deleted.")
        elif current[path] == h:
            print(f"{path} valid.")
        else:
            print(f"{path} INVALID.")

    for path in current:
        if path not in stored:
            print(f"{path} new file detected.")

def main():
    choice = input("1: Generate Hash Table\n2: Verify Hashes\nChoice: ")

    directory = input("Enter directory path: ")

    if choice == "1":
        generate_table(directory)
    elif choice == "2":
        validate_hash(directory)

main()
