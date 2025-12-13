import os
import shutil
from datetime import datetime

SOURCE_DIR = "./target"
DEST_DIR = "./archive"
DAYS_OLD = 7

def cleanup():
    if not os.path.exists(DEST_DIR):
        os.makedirs(DEST_DIR)

    now = datetime.now().timestamp()

    for file in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, file)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > DAYS_OLD * 24 * 60 * 60:
                shutil.move(file_path, os.path.join(DEST_DIR, file))
                print(f"Moved {file} to {DEST_DIR}")
            else:
                print(f"{file} is {file_age / (24 * 60 * 60):.2f} days old. Skipping.")

if __name__ == "__main__":
    cleanup()