## Python Health Service

A minimal HTTP service designed to demonstrate containerization and Kubernetes deployment patterns.

### Endpoints
- `/health` → health check endpoint for liveness/readiness probes

### Why this exists
This service is intentionally simple to focus on deployment, configuration, and reliability rather than application logic.

### Kubernetes Deployment

- Deployed using Kubernetes Deployment with 2 replicas
- Liveness and readiness probes for self-healing
- Resource requests and limits for safe scheduling
- Service exposure via ClusterIP

### Configuration Management

- Non-sensitive config via ConfigMaps
- Secrets injected via Kubernetes Secrets
- Application remains stateless and environment-agnostic
