#!/bin/bash

# Deployment validation script for Todo Chatbot Helm chart

echo "Validating Todo Chatbot deployment..."

# Check if Helm is available
if ! command -v helm &> /dev/null; then
    echo "Error: Helm is not installed"
    exit 1
fi

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed"
    exit 1
fi

# Check if there are any releases installed with the name todo-app
if helm list | grep -q "todo-app"; then
    echo "Helm release 'todo-app' exists"
else
    echo "Warning: Helm release 'todo-app' not found"
    echo "Attempting to install..."
    cd helm-chart && helm install todo-app . && cd ..
fi

# Check pods status
echo "Checking pod status..."
kubectl get pods

# Wait for pods to be ready
echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app=backend --timeout=300s

# Check services
echo "Checking services..."
kubectl get services

# Get the NodePort for frontend
NODEPORT=$(kubectl get service -l app=frontend -o jsonpath='{.items[0].spec.ports[0].nodePort}' 2>/dev/null)
if [ ! -z "$NODEPORT" ]; then
    echo "Frontend NodePort: $NODEPORT"
    echo "Frontend should be accessible at http://$(minikube ip):$NODEPORT (if using minikube)"
else
    echo "Could not get frontend NodePort"
fi

echo "Validation completed!"