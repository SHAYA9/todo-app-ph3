# Research: Kubernetes Deployment for Todo Chatbot

## Decision Points & Findings

### 1. NodePort vs Ingress for External Access

**Decision**: NodePort service for external access
**Rationale**:
- NodePort is simpler to implement and sufficient for local Minikube deployment
- No need for additional Ingress controller setup in local environment
- Direct access to frontend via NodePort aligns with requirement FR-006
- NodePort is specified in the original requirements

**Alternatives considered**:
- Ingress: Requires additional Ingress controller, more complex setup
- LoadBalancer: Not suitable for local Minikube environment
- HostPort: Less secure and harder to manage

### 2. Image Build Strategy: Inside Minikube vs External

**Decision**: Build images externally and load into Minikube
**Rationale**:
- Minikube has a built-in Docker daemon that can be accessed via `eval $(minikube docker-env)`
- Building externally and loading into Minikube is more reliable than in-cluster builds
- Easier to debug and iterate on Dockerfiles locally
- Compatible with CI/CD pipelines in future phases

**Process**:
- Build Docker images locally
- Use `minikube image load` to load images into Minikube's container registry
- Reference images in Helm chart with appropriate tags

### 3. Secret Management Approach

**Decision**: Kubernetes Secrets for database connection details
**Rationale**:
- Meets requirement FR-009 to pass database connection details as Kubernetes secrets
- Secure way to handle sensitive information in Kubernetes
- Can be mounted as volumes or environment variables to pods
- Separates sensitive configuration from application code

**Implementation**:
- Create secret manifest in Helm chart templates
- Reference secret values in deployment configurations
- Use Helm values to configure secret content during installation

### 4. Helm Chart Structure

**Decision**: Single Helm chart with multiple templates
**Rationale**:
- Meets requirement FR-003 to generate a Helm chart for deploying all application components
- Single deployment unit simplifies management
- Allows centralized configuration through values.yaml
- Follows Kubernetes best practices

**Components**:
- Frontend Deployment with 2 replicas (FR-004)
- Backend Deployment with 1 replica (FR-005)
- Frontend NodePort Service (FR-006)
- Backend ClusterIP Service (FR-007)
- ConfigMaps for environment variables (FR-008)
- Secrets for database connection (FR-009)

### 5. Service Discovery & Communication

**Decision**: Use Kubernetes DNS for internal service discovery
**Rationale**:
- Backend service will be accessible via `backend-service.default.svc.cluster.local`
- Enables internal communication between frontend and backend
- Meets requirement FR-008 to inject backend API URL to frontend
- Standard Kubernetes networking approach

### 6. Configuration Strategy

**Decision**: Environment variables via ConfigMap/Secret
**Rationale**:
- Allows dynamic configuration without rebuilding containers
- Meets requirement for environment variable injection (spec section)
- Backend API URL can be passed to frontend container
- Maintains separation of configuration from code