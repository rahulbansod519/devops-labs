import os
import shutil
from datetime import datetime
import sys

import logging
import json

# Setup logging
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }
        # Include extra fields if available
        if hasattr(record, 'action'):
            log_record['action'] = record.action
        if hasattr(record, 'file'):
            log_record['file'] = record.file
        if hasattr(record, 'source_dir'):
            log_record['source_dir'] = record.source_dir
            
        return json.dumps(log_record)

handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)

SOURCE_DIR = os.getenv("SOURCE_DIR", "/data/target")
DEST_DIR = os.getenv("DEST_DIR", "/data/archive")
DAYS_OLD = int(os.getenv("DAYS_OLD", "7"))

def cleanup():
    if not os.path.exists(SOURCE_DIR):
        logger.error("Source directory not found", extra={'source_dir': SOURCE_DIR})
        sys.exit(1)

    os.makedirs(DEST_DIR, exist_ok=True)
    now = datetime.now().timestamp()

    for file in os.listdir(SOURCE_DIR):
        file_path = os.path.join(SOURCE_DIR, file)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > DAYS_OLD * 86400:
                try:
                    shutil.move(file_path, os.path.join(DEST_DIR, file))
                    logger.info("File moved successfully", extra={'action': 'move', 'file': file})
                except Exception as e:
                    logger.error(f"Failed to move file: {str(e)}", extra={'action': 'move', 'file': file})

if __name__ == "__main__":
    cleanup()
