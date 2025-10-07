"""
Download SymSpell frequency dictionary for text correction
"""

import os
import urllib.request

def download_dictionary():
    """Download the SymSpell frequency dictionary"""
    url = "https://raw.githubusercontent.com/mammothb/symspellpy/master/symspellpy/frequency_dictionary_en_82_765.txt"
    filename = "frequency_dictionary_en_82_765.txt"
    
    if os.path.exists(filename):
        print(f"{filename} already exists")
        return
    
    print(f"Downloading {filename}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download dictionary: {e}")
        print("You can manually download it from:")
        print(url)

if __name__ == "__main__":
    download_dictionary()
