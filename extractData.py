import zipfile
import os

# Define the path to the zip file and the extraction directory
zip_file_path = 'probe_data.zip'
extraction_directory = 'probe_data'

# Create the extraction directory if it doesn't exist
os.makedirs(extraction_directory, exist_ok=True)

# Unzip the file
with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extraction_directory)

print(f'Files have been extracted to {extraction_directory}')
