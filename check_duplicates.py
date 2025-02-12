import os
import hashlib
from collections import defaultdict
from pathlib import Path

def get_file_hash(filepath):
    """Calculate MD5 hash of a file."""
    md5_hash = hashlib.md5()
    with open(filepath, "rb") as f:
        # Read file in chunks to handle large files efficiently
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def find_duplicates(directory):
    """Find duplicate files in the given directory."""
    # Dictionary to store hash -> list of files mapping
    hash_map = defaultdict(list)
    
    # Walk through all files in directory
    for root, _, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            try:
                file_hash = get_file_hash(filepath)
                hash_map[file_hash].append(filepath)
            except (IOError, OSError) as e:
                print(f"Error processing {filepath}: {e}")

    # Print duplicate files
    found_duplicates = False
    for file_hash, file_list in hash_map.items():
        if len(file_list) > 1:
            found_duplicates = True
            print("\nDuplicate files found:")
            for filepath in file_list:
                print(f"- {filepath}")
            print(f"File size: {os.path.getsize(file_list[0]) / (1024*1024):.2f} MB")
    
    if not found_duplicates:
        print("No duplicate files found.")

if __name__ == "__main__":
    downloads_path = str("./downloads")
    print(f"Checking for duplicates in: {downloads_path}")
    find_duplicates(downloads_path) 