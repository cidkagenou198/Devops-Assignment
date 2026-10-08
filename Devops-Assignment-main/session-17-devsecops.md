# Session 17: Complete CI/CD & DevSecOps

## Task 1: DevSecOps Application & Unit Test Verification

### 1. Run Unit Tests (pytest -v tests/)
Execute automated test suites across Flask REST API endpoints (health checks, greetings, arithmetic, calculator, and system status).

```bash
pytest -v tests/
```

![Unit Tests](screenshots/session17/task1-1-pytest.png)

### 2. Code Coverage Analysis (pytest --cov=app)
Measure test line coverage across all application modules to ensure test thoroughness.

```bash
pytest -v --cov=app tests/
```

![Code Coverage](screenshots/session17/task1-2-coverage.png)

---

## Task 2: SAST (Static Application Security Testing) & Quality Analysis

### 1. Bandit AST Security Scanner (bandit -r app/)
Run Bandit to scan Python Abstract Syntax Trees for common security flaws (insecure imports, SQL injection, hardcoded cryptographic keys).

```bash
bandit -r app/
```

![Bandit SAST](screenshots/session17/task2-1-sast-bandit.png)

### 2. Linting & PEP 8 Style Enforcement (flake8 app/)
Enforce strict code quality, unused import detection, and complexity checks via Flake8.

```bash
flake8 app/ --max-line-length=120
```

![Flake8 Lint](screenshots/session17/task2-2-lint-flake8.png)

---

## Task 3: Secret Scanning & Credential Exposure Detection

### 1. Secret Pattern & Credential File Audit
Scan repository directory trees for sensitive credential formats (`.env`, `*.pem`, `*.key`, `id_rsa`).

```bash
powershell -Command "Get-ChildItem -Recurse -Include *.env,*.pem,*.key | Select-Object Name"
```

![Secret File Audit](screenshots/session17/task3-1-secret-scanning.png)

### 2. High-Entropy Git History Scanning (gitleaks)
Scan commits and working trees for leaked API keys, tokens, or plaintext passwords using Gitleaks rules.

```bash
gitleaks detect --source . --verbose
```

![Gitleaks Scan](screenshots/session17/task3-2-entropy-scan.png)

---

## Task 4: Software Composition Analysis (SCA) & Dependency Audit

### 1. Dependency Manifest Inspection
Review declared production and development requirements for version pins.

```bash
type requirements.txt requirements-dev.txt
```

![Dependencies](screenshots/session17/task4-1-sca-audit.png)

### 2. Safety / CVE Dependency Vulnerability Check
Audit all third-party dependencies against the Python Packaging Advisory Database for known Common Vulnerabilities and Exposures (CVEs).

```bash
safety check -r requirements.txt
```

![SCA Quality Gate](screenshots/session17/task4-2-sca-remediation.png)

---

## Task 5: Container Image Scanning & Vulnerability Assessment

### 1. Docker Container Image Build
Build the hardened container image using a multi-stage, non-root Python runtime base.

```bash
docker build -t devsecops-demo:latest .
```

![Docker Build](screenshots/session17/task5-1-docker-build.png)

### 2. Container Vulnerability Assessment (Trivy)
Execute Trivy container image scan targeting OS packages and application dependencies to enforce zero-critical vulnerability policies.

```bash
trivy image --severity HIGH,CRITICAL devsecops-demo:latest
```

![Trivy Image Scan](screenshots/session17/task5-2-container-scan.png)

---

## Task 6: Kubernetes Deployment & Security Gate Enforcement

### 1. Kubernetes Dry-Run Manifest Validation
Validate Kubernetes Deployment and Service definitions via client-side schema verification before applying changes.

```bash
kubectl apply --dry-run=client -f k8s/
```

![Kubernetes Dry-Run](screenshots/session17/task6-1-k8s-dry-run.png)

### 2. Cluster Deployment & Pod Health Verification
Deploy the verified application container to the cluster, confirming pod readiness and service endpoint registration.

```bash
kubectl apply -f k8s/
```

![Kubernetes Deployment](screenshots/session17/task6-2-k8s-deployment.png)

### 3. Teardown & Cluster Cleanup
Safely decommission deployed Kubernetes resources after verification testing.

```bash
kubectl delete -f k8s/
```

![Kubernetes Cleanup](screenshots/session17/task6-3-k8s-cleanup.png)
