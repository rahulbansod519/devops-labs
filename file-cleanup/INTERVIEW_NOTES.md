# DevOps Interview Notes

## 1. Why Job vs CronJob?
**Job** objects in Kubernetes are designed for finite, run-to-completion tasks. They are perfect for:
- Database migrations.
- Batch processing a specific dataset.
- Manual triggers of automated tasks.

**CronJobs** are time-based schedulers that create Jobs. They are chosen for this project because:
- **Automation**: File cleanup is a maintenance task that should happen periodically (e.g., daily) without human intervention.
- **Resource Efficiency**: Unlike a long-running "sidecar" or daemon process that sleeps for 23 hours, a CronJob spins up a Pod only when needed and terminates it after completion, freeing up cluster resources.

## 2. How does your CI pipeline protect production?
The configured GitHub Actions workflow acts as a gatekeeper:
- **Automated Verification**: Every push and pull request triggers the `pytest` suite.
- **Fail Fast**: If a developer breaks the logic (e.g., syntax error or regression in file selection), the build fails immediately.
- **Preventing Bad Merges**: By requiring status checks to pass before merging to `main`, we ensure that broken code never reaches the production branch or the deployment stage.

## 3. How would you debug a failed CronJob?
Debugging follows a systematic "drill-down" approach:
1.  **Check Status**: `kubectl get cronjobs` to see LAST SCHEDULE and ACTIVE status.
2.  **Find the Job**: `kubectl get jobs` lists the actual executions created by the CronJob.
3.  **Find the Pod**: `kubectl get pods --selector=job-name=<job-name>` to find the specific pod implementation.
4.  **Inspect Logs**: `kubectl logs <pod-name>` is the first step to see application-level errors (like our "Source directory not found").
5.  **Inspect Events**: If the pod didn't start, `kubectl describe pod <pod-name>` reveals infrastructure issues like `ImagePullBackOff`, `CrashLoopBackOff`, or `MountPropagation` errors.

## 4. Why environment variables over hardcoding?
Using environment variables (`SOURCE_DIR`, `DAYS_OLD`) adheres to the **12-Factor App** methodology:
- **Portability**: The same container image can be used in Dev, Staging, and Prod with different configurations (e.g., 7 days retention in Prod vs 1 day in Dev).
- **Security**: Secrets and sensitive paths aren't committed to version control.
- **Flexibility**: Behavior can be tuned by Ops teams via Kubernetes manifests without needing to modify source code or rebuild the Docker image.

## 5. How does this scale?
Currently, the script is single-threaded. Scaling challenges and solutions include:
- **Volume of Files**: For millions of files, a simple `os.listdir` might be slow or memory-intensive.
    - *Solution*: Use `os.scandir` (iterator) or shard the work across multiple Jobs processing different subdirectories.
- **Storage Access**: Heavy I/O might impact other services sharing the storage.
    - *Solution*: Schedule the CronJob during off-peak hours (already done via "0 2 * * *").

## 6. What tradeoffs did you make?
- **HostPath vs PVC**: I used `hostPath` for the Kubernetes volume.
    - *Pros*: Simple to set up on a local machine (Docker Desktop/Minikube).
    - *Cons*: Not portable to multi-node clusters (pod must land on the specific node with the files). In a real cluster, I would use a `PersistentVolumeClaim` (PVC) with `ReadWriteMany` access mode.
- **Python vs Go/Rust**: I chose Python for speed of development and readability.
    - *Pros*: Easy to write and maintain; rich libraries.
    - *Cons*: Slower execution speed than compiled languages, though usually negligible for file system operations where I/O is the bottleneck.
