## File Cleanup Automation

A simple Python script that automatically moves files older than a defined number of days to an archive directory.

### Why this matters
This mimics real-world DevOps housekeeping tasks such as log rotation and storage management.

### Tech
- Python
- Docker
- Kubernetes
- GitHub Actions (CI)

### Key Features
- **Automated Cleanup**: Deletes/Moves files older than a specified duration.
- **Structured Logging**: Outputs logs in JSON format for easy ingestion by observability tools (ELK, Datadog).
- **CI/CD Integrated**: Automated testing on every push using GitHub Actions.

### Environment Variables
- `SOURCE_DIR`: Directory to scan (default: `/data/target`)
- `DEST_DIR`: Archive location (default: `/data/archive`)
- `DAYS_OLD`: File age threshold in days (default: `7`)

### Docker Usage

```bash
docker build -t file-cleanup .
docker run \
  -e DAYS_OLD=7 \
  -v /host/target:/data/target \
  -v /host/archive:/data/archive \
  file-cleanup

### Kubernetes Usage

This project includes Kubernetes manifests for both a one-time Job and a scheduled CronJob.

#### Why CronJob?

For tasks like file cleanup, a **CronJob** is superior to a long-running pod because:
1.  **Resource Efficiency**: The pod only runs when needed (e.g., once a day), freeing up CPU and RAM for other applications during idle times.
2.  **Reliability**: Kubernetes handles retries and scheduling automatically. If the node fails, the job is rescheduled.
3.  **Simplicity**: No need to implement complex sleep/wake logic or scheduling libraries within the application code.

#### Job vs CronJob

- **Job**: Use for a one-off task (e.g., initial data migration, manual cleanup trigger).
- **CronJob**: Use for recurring tasks (e.g., daily log rotation, nightly backups).

#### Real-World Application

This pattern maps directly to essential infrastructure tasks:
- **Log Rotation**: cleaning up old logs to prevent disk saturation.
- **Storage Hygiene**: Archiving old backups or temporary files to cheaper storage tiers.
- **Compliance**: Enforcing data retention policies by deleting data older than a specific period.

