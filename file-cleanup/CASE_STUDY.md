# File Cleanup Automation – DevOps Case Study

## Problem
In many systems, logs and temporary files accumulate over time, leading to wasted storage and operational risk. Manual cleanup is unreliable and error-prone.

## Solution
I built a containerized file cleanup utility that automatically archives files older than a configurable number of days. The system runs as a Kubernetes Job for validation and as a CronJob for scheduled execution.

## Architecture
- Python for file system automation
- Docker for portability
- Kubernetes Job for one-time execution
- Kubernetes CronJob for scheduled runs
- Environment variables for configuration
- Volumes for safe file access
- GitHub Actions for CI validation

## Execution Flow
1. Code is pushed to GitHub
2. CI pipeline validates the build
3. Container image is executed as a Kubernetes Job
4. CronJob schedules periodic cleanup
5. Logs are emitted to stdout for observability

## Failure Handling
- Job fails fast if source directory is missing
- CronJob retries on failure
- Logs enable fast root cause analysis

## What I’d Improve Next
- Add unit tests for file selection logic
- Push image to a registry automatically
- Add metrics for files cleaned per run
