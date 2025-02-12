#!/usr/bin/env python3

import os
import shutil
import random
from pathlib import Path

# Source and destination directories
source_dir = Path('downloads')
dest_dir = Path('/Volumes/X7')

def copy_files_with_random_prefix():
    # Get all WAV files from source directory
    wav_files = list(source_dir.rglob('*.wav'))  # Using rglob to search recursively in all subdirectories
    # print(wav_files)
    # Create a list of random numbers for prefixes (10, 20, 30, ...)
    # Making the step 10 to have nice round numbers
    random_numbers = list(range(10, (len(wav_files) + 1) * 10, 10))
    # Shuffle the numbers
    random.shuffle(random_numbers)
    
    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Found {len(wav_files)} WAV files to copy...")
    
    # Copy each file with a random prefix
    for file_path, number in zip(wav_files, random_numbers):
        # Create new filename with random prefix and ensure only ASCII alphanumeric chars
        # Arabic to English transliteration mapping
        ar_to_en = {
            'ا': 'a', 'أ': 'a', 'إ': 'e', 'ى': 'a', 'ب': 'b', 'ت': 't',
            'ث': 'th', 'ج': 'j', 'ح': 'h', 'خ': 'kh', 'د': 'd', 'ذ': 'th',
            'ر': 'r', 'ز': 'z', 'س': 's', 'ش': 'sh', 'ص': 's', 'ض': 'd',
            'ط': 't', 'ظ': 'z', 'ع': 'a', 'غ': 'gh', 'ف': 'f', 'ق': 'q',
            'ك': 'k', 'ل': 'l', 'م': 'm', 'ن': 'n', 'ه': 'h', 'و': 'w',
            'ي': 'y', 'ئ': 'e', 'ء': '', 'ؤ': 'o', 'ة': 'h', 'َ': 'a',
            'ُ': 'u', 'ِ': 'i', 'ﷺ': 'alayhisalaam', 'ﷲ': 'allah'
        }
        # Transliterate Arabic characters and keep ASCII alphanumeric
        base_name = ''
        for c in file_path.stem:
            if c in ar_to_en:
                base_name += ar_to_en[c]
            elif c.isalnum() and ord(c) < 128:
                base_name += c.lower()
            elif c == ' ':
                base_name += ' '
        base_name = base_name + file_path.suffix
        new_filename = f"{number:03d}_{base_name}"
        dest_path = dest_dir / new_filename
        
        print(f"Copying {file_path.name} -> {new_filename}")
        shutil.copy2(file_path, dest_path)
    
    print("\nCopying complete!")

if __name__ == '__main__':
    try:
        copy_files_with_random_prefix()
    except Exception as e:
        print(f"An error occurred: {e}") 