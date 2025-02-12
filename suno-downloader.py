# Usage: python suno-downloader.py <path-to-js-output-file>
import requests
import os
import sys

def download_file(url, filename):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def main():
    js_file = sys.argv[1]
    with open(js_file, 'r') as file:
        js_output = file.read()


    # Split the input string into individual file entries
    file_entries = js_output.split("\n")

    # Create a directory to store the downloaded files
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    names = ()
    # Process each file entry
    for entry in file_entries:
        try:
            i = 0
            print(f"Processing: {entry}")
            filename, url = entry.split('|')
            print(f"Downloading: {filename}")
            org_name =  os.path.splitext(filename)[0]
            ext = os.path.splitext(filename)[1]
            # make sure the file name is unique
            while filename in names:
                i += 1
                name = org_name + "_" + str(i)
                filename = name + ext

            names = names + (filename,)




            download_file(url, os.path.join('downloads', filename))
            print(f"Successfully downloaded: {filename}")
        except Exception as e:
            print(f"Failed to download {entry}. Error: {str(e)}")

    print("Download process completed.")

if __name__ == "__main__":
    main()
