import os
import hashlib
import json

HASH_FILE = "hash_table.json"

def hash_file(filepath):
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def traverse_directory(directory):
    file_hashes = {}

    for root, _, files in os.walk(directory):
        for name in files:
            if name == HASH_FILE:
                continue

            path = os.path.join(root, name)
            try:
                file_hashes[path] = hash_file(path)
            except:
                print(f"Could not read {path}")

    return file_hashes

def generate_table():
    directory = input("Enter directory path: ").strip()

    if not os.path.isdir(directory):
        print("Invalid directory.")
        return

    hashes = traverse_directory(directory)

    with open(HASH_FILE, "w") as f:
        json.dump(hashes, f, indent=4)

    print("Hash table generated.")

def validate_hashes():
    if not os.path.exists(HASH_FILE):
        print("No hash table found.")
        return

    directory = input("Enter directory path: ").strip()

    with open(HASH_FILE, "r") as f:
        stored_hashes = json.load(f)

    current_hashes = traverse_directory(directory)

    for path, old_hash in stored_hashes.items():
        if path not in current_hashes:
            print(f"{path} -> FILE DELETED")
        else:
            if current_hashes[path] == old_hash:
                print(f"{path} -> VALID")
            else:
                print(f"{path} -> INVALID")

    for path in current_hashes:
        if path not in stored_hashes:
            print(f"{path} -> NEW FILE")

def main():
    print("1. Create hash table")
    print("2. Verify hashes")

    choice = input("Choose: ")

    if choice == "1":
        generate_table()
    elif choice == "2":
        validate_hashes()
    else:
        print("Invalid choice.")

main()
