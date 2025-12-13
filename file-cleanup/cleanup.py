import os
import shutil
from datetime import datetime
import sys

SOURCE_DIR = os.getenv("SOURCE_DIR", "/data/target")
DEST_DIR = os.getenv("DEST_DIR", "/data/archive")
DAYS_OLD = int(os.getenv("DAYS_OLD", "7"))

def cleanup():
    if not os.path.exists(SOURCE_DIR):
        print(f"Source directory not found: {SOURCE_DIR}")
        sys.exit(1)

    os.makedirs(DEST_DIR, exist_ok=True)
    now = datetime.now().timestamp()

    for file in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, file)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > DAYS_OLD * 86400:
                shutil.move(file_path, os.path.join(DEST_DIR, file))
                print(f"Moved: {file}")

if __name__ == "__main__":
    cleanup()
