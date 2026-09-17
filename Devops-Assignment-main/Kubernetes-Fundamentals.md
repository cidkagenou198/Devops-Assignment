# Kubernetes Basic Commands

Simple Kubernetes command reference for learning and practice.

---

## 1. Minikube

```bash
# Start cluster
minikube start

# Check status
minikube status

# Stop cluster
minikube stop

# Delete cluster
minikube delete

# Get Minikube IP
minikube ip

# Open dashboard
minikube dashboard

# List addons
minikube addons list
````

---

## 2. Cluster

```bash
# Cluster information
kubectl cluster-info

# Kubernetes version
kubectl version

# Client version
kubectl version --client

# Get nodes
kubectl get nodes

# Detailed node information
kubectl describe node <node-name>
```

---

## 3. Basic kubectl

```bash
# Get all resources
kubectl get all

# Get resource
kubectl get <resource>

# Detailed information
kubectl describe <resource> <name>

# Get YAML
kubectl get <resource> <name> -o yaml

# Get JSON
kubectl get <resource> <name> -o json

# Watch changes
kubectl get pods -w

# Get resources from all namespaces
kubectl get pods -A
```

---

## 4. Pods

```bash
# List Pods
kubectl get pods

# Detailed Pods
```
