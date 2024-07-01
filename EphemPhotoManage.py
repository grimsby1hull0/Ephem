import os
import re
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm
from time import sleep
import threading

class Color:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\x1b[46m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

# ASCII art of Ephem
EPHEM_ASCII = """
  __
(o.o)
(/|\\)
  ^
"""

# Supported file extensions
PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.heic', '.heif', '.psd', '.svg'}
RAW_EXTENSIONS = {'.raw', '.arw', '.cr2', '.nef', '.orf', '.sr2', '.dng', '.rw2', '.pef', '.srw', '.x3f', '.crw'}
DOCUMENT_EXTENSIONS = {'.pdf', '.txt', '.doc', '.docx', '.odt', '.rtf', '.md', '.html', '.htm', '.xml', '.json', '.csv', '.xls', '.xlsx', '.ppt', '.pptx'}

def get_photo_date(photo_path):
    try:
        image = Image.open(photo_path)
        info = image._getexif()
        if info is not None:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "DateTimeOriginal":
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Error getting date for {photo_path}: {e}")
    return None

def extract_date_from_title(filename):
    date_patterns = [
        r'(\d{4})[-_](\d{2})[-_](\d{2})',  # yyyy-mm-dd or yyyy_mm_dd
        r'(\d{4})(\d{2})(\d{2})',          # yyyymmdd
        r'(\d{2})[-_](\d{2})[-_](\d{4})',  # dd-mm-yyyy or dd_mm_yyyy
    ]
    for pattern in date_patterns:
        match = re.search(pattern, filename)
        if match:
            try:
                if len(match.groups()) == 3:
                    if len(match.group(1)) == 4:
                        # yyyy-mm-dd or yyyy_mm_dd or yyyymmdd
                        return datetime.strptime(''.join(match.groups()), "%Y%m%d")
                    else:
                        # dd-mm-yyyy or dd_mm_yyyy
                        return datetime.strptime(''.join(match.groups()), "%d%m%Y")
            except ValueError:
                continue
    return None

def simulate_file_transfers():
    total_files = 100
    print("Simulating file transfers...")
    for _ in tqdm(range(total_files), desc="Transferring files", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"):
        sleep(0.05)
    

def organize_photos(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    unsorted_folder = os.path.join(target_folder, "Unsorted")
    if not os.path.exists(unsorted_folder):
        os.makedirs(unsorted_folder)

    files_folder = os.path.join(target_folder, "Files")
    if not os.path.exists(files_folder):
        os.makedirs(files_folder)

    raw_subfolder_name = "RAW"
    raw_folder = os.path.join(target_folder, raw_subfolder_name)
    if not os.path.exists(raw_folder):
        os.makedirs(raw_folder)

    # Collect all files to be organized
    files_to_organize = []
    for root, _, files in os.walk(source_folder):
        for filename in files:
            file_path = os.path.join(root, filename)
            if os.path.isfile(file_path):
                files_to_organize.append((filename, file_path))

    # Progress bar setup
    total_files = len(files_to_organize)
    pbar = tqdm(total=total_files, desc="Organizing files", ncols=100, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} files")

    for filename, file_path in files_to_organize:
        if os.path.isfile(file_path):
            ext = os.path.splitext(filename)[1].lower()
            if ext in PHOTO_EXTENSIONS:
                photo_date = get_photo_date(file_path)
                if photo_date is None and ext == ".dng":
                    photo_date = extract_date_from_title(filename)
                if photo_date:
                    year = photo_date.year
                    month = photo_date.strftime("%B")
                    target_dir = os.path.join(target_folder, str(year), month)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)
                    shutil.move(file_path, os.path.join(target_dir, filename))
                else:
                    shutil.move(file_path, os.path.join(unsorted_folder, filename))
            elif ext in RAW_EXTENSIONS:
                raw_file_folder = os.path.join(raw_folder, filename)
                shutil.move(file_path, raw_file_folder)
            elif ext in DOCUMENT_EXTENSIONS:
                shutil.move(file_path, os.path.join(files_folder, filename))
            else:
                shutil.move(file_path, os.path.join(unsorted_folder, filename))
            pbar.update(1)
            print(f"Moved {filename}")

    pbar.close()

if __name__ == "__main__":
    # Print ASCII art of Ephem
    print(EPHEM_ASCII)
    
    # Greeting message
    print(f"{Color.CYAN}Hello!{Color.END} Welcome to Ephem's Photo Organisation tool!\n")
    
    while True:
        source_folder = input("Please enter the source folder path: ").strip()
        if source_folder.lower() == "linux":
            print("Thanks :)")
            sleep(0.5)
            simulate_file_transfers()
            break
        if not source_folder:
            print("Oops, I don't think you put anything in, try again maybe :)")
            continue
        target_folder = input("Alongside the path to your destination folder: ").strip()
        if not target_folder:
            print("Oops, I don't think you put anything in, try again maybe :)")
            continue
        print("Thanks :)")
        sleep(0.5)
        organize_photos(source_folder, target_folder)
        break

    # Ephem's dance
    ephem_dance = [
        """
  __
(o.o)
(/|\\)
  ^
        """,
        """
  __
(o.o)
(\|/)
  ^
        """
    ]

    print("\nThe organisational process was successful!\n")

    def dance_ephem():
        while True:
            for frame in ephem_dance:
                print(frame)
                print("Thanks for using Ephem, Press ENTER to finish the script :)")
                sleep(0.5)
                if input() == '':
                    return

    dance_thread = threading.Thread(target=dance_ephem)
    dance_thread.start()
    dance_thread.join()
