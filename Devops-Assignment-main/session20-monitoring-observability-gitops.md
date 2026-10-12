# Session 20: Monitoring, Observability & GitOps

This session covers enterprise observability architectures (Metrics, Logs, and Traces), Prometheus pull-based time-series scraping, Grafana dashboards, and GitOps automation with Argo CD on Kubernetes. Topics include self-healing reconciliations, declarative application manifests, and full cluster workload lifecycle management.

---

# Task 1: Monitoring vs Observability Architecture

## 1. Inspect Monitoring vs Observability Foundations
Understand the core architectural distinction between alerting on known failure thresholds (Monitoring) and inferring systemic internal health through telemetry (Observability):

```bash
head -n 22 01-monitoring-vs-observability/README.md
```

![Monitoring vs Observability](screenshots/session20/task1-1-monitoring-vs-observability.png)

## 2. Inspect the Three Pillars of Observability
Review the roles and design characteristics of Metrics, Logs, and Traces in distributed cloud-native systems:

```bash
cat 02-metrics-logs-traces/README.md | head -n 25
```

![Three Pillars](screenshots/session20/task1-2-pillars-inspect.png)

---

# Task 2: Prometheus Setup & Scraping

## 1. Inspect Prometheus Compose definition
Inspect service specification mounting `prometheus.yml` configuration and exposing metrics endpoint on port 9090:

```bash
cat docker-compose.yml
```

![Prometheus Compose](screenshots/session20/task2-1-prom-compose.png)

## 2. Inspect Prometheus scrape configuration
Review scrape interval and static target configurations in `prometheus.yml`:

```bash
cat prometheus.yml
```

![Prometheus Config](screenshots/session20/task2-2-prom-config.png)

## 3. Launch Prometheus server
Start the Prometheus container in detached mode and verify running container status:

```bash
docker compose up -d && docker compose ps
```

![Prometheus Running](screenshots/session20/task2-3-prom-running.png)

## 4. Query live Prometheus metrics
Query the Prometheus endpoint to retrieve time-series counters and HTTP request metrics:

```bash
curl -s http://localhost:9090/metrics | grep -E '^# TYPE prometheus_http_requests_total' -A 3
```

![Prometheus Metrics](screenshots/session20/task2-4-prom-metrics.png)

## 5. Prometheus Expression Browser Web UI
Open `http://localhost:9090` to execute PromQL queries (`up`, `process_cpu_seconds_total`) and observe real-time time-series evaluations in Table and Graph views:

```bash
# Access Prometheus UI in browser:
http://localhost:9090
```

![Prometheus Web UI](screenshots/session20/task2-5-prometheus-web-ui.png)

---

# Task 3: Grafana Visualization Stack

## 1. Inspect unified Grafana & Prometheus Compose definition
Review the integrated telemetry visualization stack configuring Grafana (port 3000) with Prometheus as upstream datasource:

```bash
cat docker-compose.yml
```

![Grafana Compose](screenshots/session20/task3-1-grafana-compose.png)

## 2. Start observability telemetry stack
Bring up both Prometheus and Grafana microservices and verify health status:

```bash
docker compose up -d && docker compose ps
```

![Grafana Stack Running](screenshots/session20/task3-2-grafana-stack.png)

## 3. Configure Grafana Telemetry Dashboard
Open Grafana (`http://localhost:3000`), connect Prometheus datasource, and construct visual panels for TSDB chunks, health status (`up`), and CPU utilization gauge:

```bash
# Access Grafana Dashboard:
http://localhost:3000
```

![Grafana Dashboard](screenshots/session20/task3-3-grafana-dashboard.png)

---

# Task 4: Git as Source of Truth

## 1. Inspect GitOps Deployment manifest
Review the declarative Kubernetes Deployment manifest maintained in Git as the definitive system state:

```bash
cat deployment.yaml
```

![GitOps Deployment](screenshots/session20/task4-1-git-manifest.png)

## 2. Inspect GitOps Service manifest
Review the declarative Kubernetes Service manifest exposing cluster workloads:

```bash
cat service.yaml
```

![GitOps Service](screenshots/session20/task4-2-git-service.png)

---

# Task 5: Argo CD Declarative Application

## 1. Inspect Argo CD Custom Resource definition
Review the `argoproj.io/v1alpha1` Application manifest configuring automated synchronization, target revision, and self-healing policies:

```bash
cat app/argocd-application.yaml
```

![Argo CD App Yaml](screenshots/session20/task5-1-argocd-app-yaml.png)

## 2. Verify Argo CD synchronization status
Inspect the Argo CD application status via CLI to verify cluster synchronization and health:

```bash
kubectl get applications -n argocd
```

![Argo CD Sync Status](screenshots/session20/task5-2-argocd-sync-status.png)

## 3. Argo CD Application Overview Web UI
Access the Argo CD web dashboard (`http://localhost:8080`) to inspect the synchronized `session20-app` tile displaying Health (`Healthy`), Sync Status (`Synced`), and Git repository commit tracking:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

![Argo CD Applications UI](screenshots/session20/task5-3-argocd-applications-ui.png)

---

# Task 6: Mini-Project GitOps Deployment & Reconciliation

## 1. Inspect mini-project production deployment manifest
Inspect the multi-replica workload manifest targeted for automated GitOps deployment:

```bash
cat app/deployment.yaml
```

![Mini Project Deployment](screenshots/session20/task6-1-mini-deploy-yaml.png)

## 2. Inspect running cluster workloads
Verify that Kubernetes workloads are deployed with target pod replica counts:

```bash
kubectl get all -n session20
```

![Kubernetes Workload](screenshots/session20/task6-2-mini-k8s-workload.png)

## 3. Verify GitOps self-healing and drift correction
Manually introduce cluster drift by downscaling replicas; observe Argo CD detecting drift and automatically restoring desired state from Git:

```bash
kubectl scale deployment session20-mini -n session20 --replicas=1 && sleep 2 && kubectl get deployment -n session20
```

![GitOps Self Healing](screenshots/session20/task6-3-gitops-self-healing.png)

## 4. Argo CD Live Workload Topology & Resource Tree
Inspect the live resource tree in Argo CD showing declarative GitOps relationships spanning Application $\rightarrow$ Service + Deployment $\rightarrow$ ReplicaSet $\rightarrow$ Pods:

```bash
# View Application Topology in Argo CD:
http://localhost:8080/applications/session20-app
```

![Argo CD Topology Tree](screenshots/session20/task6-5-argocd-resource-tree-ui.png)

## 5. Teardown & cleanup
Tear down the observability stack and clean up Kubernetes namespace:

```bash
docker compose -f 04-grafana/docker-compose.yml down && kubectl delete namespace session20
```

![Cleanup](screenshots/session20/task6-4-cleanup.png)
