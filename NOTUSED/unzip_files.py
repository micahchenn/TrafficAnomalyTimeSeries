import zipfile
import os

def unzip_file(zip_path, extract_to):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

if __name__ == "__main__":
    zip_path = 'data.zip'  # Path to your zip file
    extract_to = 'extracted_data'  # Directory to extract to

    if not os.path.exists(extract_to):
        os.makedirs(extract_to)

    unzip_file(zip_path, extract_to)
    print(f"Files extracted to {extract_to}")
