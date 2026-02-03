# Data Model: Kubernetes Deployment

## Kubernetes Resources

### Frontend Deployment
- **Name**: frontend-deployment
- **Replicas**: 2 (as per requirement FR-004)
- **Container**: Next.js application container
- **Image**: todo-frontend:latest (to be built and tagged)
- **Environment Variables**:
  - BACKEND_API_URL: URL of backend service
- **Ports**: Exposes port 3000 (Next.js default)

### Backend Deployment
- **Name**: backend-deployment
- **Replicas**: 1 (as per requirement FR-005)
- **Container**: FastAPI application container
- **Image**: todo-backend:latest (to be built and tagged)
- **Environment Variables**:
  - DATABASE_URL: Reference to database connection secret
- **Ports**: Exposes port 8000 (FastAPI default)

### Frontend Service
- **Name**: frontend-service
- **Type**: NodePort (as per requirement FR-006)
- **Target Port**: 3000
- **Node Port**: Dynamically assigned or configurable
- **Selector**: Matches frontend deployment

### Backend Service
- **Name**: backend-service
- **Type**: ClusterIP (as per requirement FR-007)
- **Target Port**: 8000
- **Selector**: Matches backend deployment

### Configuration Secret
- **Name**: db-config-secret
- **Data**:
  - database-url: Base64 encoded database connection string
- **Usage**: Mounted as environment variable to backend container

### ConfigMap
- **Name**: app-config
- **Data**:
  - BACKEND_API_URL: http://backend-service:8000 (internal Kubernetes DNS)

## Deployment Relationships

### Network Flow
1. External users connect to frontend via NodePort
2. Frontend communicates with backend via ClusterIP service
3. Backend connects to database via secret configuration

### Resource Dependencies
- Frontend deployment depends on backend service availability
- Backend deployment depends on database secret
- Both deployments depend on their respective services

## Scaling Characteristics

### Frontend
- Horizontal scaling: 2 replicas as baseline
- Load balancing: Distributed across available nodes
- Session management: Stateless (Next.js SSR)

### Backend
- Horizontal scaling: Currently 1 replica (can be scaled based on demand)
- Load balancing: Kubernetes internal load balancing
- State management: Stateless API layer