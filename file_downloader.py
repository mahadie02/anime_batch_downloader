import os
import requests
from tqdm import tqdm

def download_file(url, dest_folder, new_filename):
    # Ensure the destination folder exists
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Get the full file path
    file_path = os.path.join(dest_folder, new_filename)
    
    # Send a request to the URL and get the file size
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    # Download the file with a progress bar
    with open(file_path, 'wb') as file, tqdm(
        desc=new_filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            file.write(data)
            progress_bar.update(len(data))
    
    print(f"Download completed.\n")
