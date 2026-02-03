# Quickstart: Kubernetes Deployment

## Prerequisites

- Docker Desktop installed and running
- Minikube installed and configured
- kubectl installed and configured
- Helm 3+ installed
- Node.js and npm (for local development)

## Setup Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Set Docker environment to Minikube
```bash
eval $(minikube docker-env)
```

### 3. Build Docker Images
```bash
# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..
```

### 4. Install Helm Chart
```bash
# Navigate to helm chart directory
cd helm-chart

# Install the chart
helm install todo-app .
```

### 5. Access the Application
```bash
# Get the NodePort URL
minikube service frontend-service --url

# Or access via tunnel (recommended for persistent access)
minikube tunnel
```

## Verification Steps

1. Check all pods are running:
```bash
kubectl get pods
```

2. Verify services are available:
```bash
kubectl get services
```

3. Access frontend via browser using the NodePort URL from step 5 above

4. Test chatbot functionality by interacting with the UI

## Troubleshooting

- If pods fail to start, check logs:
```bash
kubectl logs -l app=frontend
kubectl logs -l app=backend
```

- If services aren't accessible, verify NodePort assignment:
```bash
kubectl describe service frontend-service
```

- To uninstall the application:
```bash
helm uninstall todo-app
```

## Development Workflow

1. Make changes to frontend/backend code
2. Rebuild Docker images with new tags
3. Update Helm chart values to use new image tags
4. Upgrade Helm release:
```bash
helm upgrade todo-app .
```