# Todo Chatbot Helm Chart

This Helm chart deploys the Todo Chatbot application to Kubernetes, consisting of a Next.js frontend and FastAPI backend.

## Prerequisites

- Kubernetes 1.28+
- Helm 3+

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
helm install todo-app .
```

## Uninstalling the Chart

To uninstall the `todo-app` deployment:

```bash
helm uninstall todo-app
```

## Configuration

The following table lists the configurable parameters of the todo-chatbot chart and their default values.

| Parameter                     | Description                                             | Default                |
|-------------------------------|---------------------------------------------------------|------------------------|
| `frontend.replicaCount`       | Number of frontend replicas                             | `2`                    |
| `frontend.image.repository`   | Frontend image repository                               | `todo-frontend`        |
| `frontend.image.tag`          | Frontend image tag                                      | `latest`               |
| `frontend.image.pullPolicy`   | Frontend image pull policy                              | `IfNotPresent`         |
| `frontend.service.type`       | Frontend service type                                   | `NodePort`             |
| `frontend.service.port`       | Frontend service port                                   | `3000`                 |
| `frontend.env.BACKEND_API_URL`| Backend API URL for frontend                            | `"http://backend-service:8000"` |
| `backend.replicaCount`        | Number of backend replicas                              | `1`                    |
| `backend.image.repository`    | Backend image repository                                | `todo-backend`         |
| `backend.image.tag`           | Backend image tag                                       | `latest`               |
| `backend.image.pullPolicy`    | Backend image pull policy                               | `IfNotPresent`         |
| `backend.service.type`        | Backend service type                                    | `ClusterIP`            |
| `backend.service.port`        | Backend service port                                    | `8000`                 |
| `backend.env.DATABASE_URL`    | Database URL for backend                                | `""`                   |

## Example Values File

Create a `values.yaml` file to customize the deployment:

```yaml
frontend:
  replicaCount: 3
  image:
    repository: my-repo/todo-frontend
    tag: v1.0.0

backend:
  replicaCount: 2
  image:
    repository: my-repo/todo-backend
    tag: v1.0.0
  env:
    DATABASE_URL: "postgresql://user:pass@db:5432/todo_db"
```

Then install with:

```bash
helm install todo-app -f values.yaml .
```

## Deployment Validation

After installation, verify the deployment:

```bash
kubectl get pods
kubectl get services
```

The frontend should be accessible via the NodePort service.