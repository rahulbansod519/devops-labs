## File Cleanup Automation

A simple Python script that automatically moves files older than a defined number of days to an archive directory.

### Why this matters
This mimics real-world DevOps housekeeping tasks such as log rotation and storage management.

### Tech
- Python

### Docker Usage

```bash
docker build -t file-cleanup .
docker run \
  -e DAYS_OLD=7 \
  -v /host/target:/data/target \
  -v /host/archive:/data/archive \
  file-cleanup

