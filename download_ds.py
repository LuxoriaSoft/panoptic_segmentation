import os
import urllib.request
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Function to download a file from a given URL
def download_file(url, dest_folder):
    # Create destination folder if it does not exist
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    # Get the file name from the URL
    file_name = os.path.join(dest_folder, url.split('/')[-1])
    
    # Check if the file already exists to avoid redundant downloads
    if os.path.exists(file_name):
        print(f"{file_name} already exists")
        return
    
    # Open the URL and download the file in chunks
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        total_size = int(response.info().get("Content-Length", 0))  # Get the total file size
        chunk_size = 1024 * 1024  # Set chunk size to 1MB
        
        # Display progress bar while downloading
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=file_name) as pbar:
            while True:
                chunk = response.read(chunk_size)
                if not chunk:
                    break
                out_file.write(chunk)
                pbar.update(len(chunk))  # Update progress bar

# Function to download the COCO dataset
def download_coco_dataset():
    urls = [
        "http://images.cocodataset.org/zips/train2017.zip",
        "http://images.cocodataset.org/zips/val2017.zip",
        "http://images.cocodataset.org/annotations/panoptic_annotations_trainval2017.zip"
    ]
    dest_folder = "."  # Set destination folder
    
    # Use multithreading to download files concurrently
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(lambda url: download_file(url, dest_folder), urls)

# Run the download function if the script is executed directly
if __name__ == "__main__":
    download_coco_dataset()
