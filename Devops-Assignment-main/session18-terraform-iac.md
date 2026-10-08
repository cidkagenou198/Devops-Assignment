# Session 18: Terraform & Infrastructure as Code

## Task 1: Terraform Workflow Initialization & Formatting

### 1. Initialize Terraform Providers & Backend (terraform init)
Initialize the working directory containing Terraform configuration files. Downloads provider plugins and configures state backend.

```bash
cd terraform-s3-demo
terraform init
```

![Terraform Init](screenshots/session18/task1-1-tf-init.png)

### 2. Format Configuration Code (terraform fmt -check)
Enforce standard HCL indentation, canonical alignment, and syntax readability.

```bash
terraform fmt -check
```

![Terraform Fmt](screenshots/session18/task1-2-tf-fmt.png)

### 3. Validate Configuration Semantics (terraform validate)
Verify that the configuration is syntactically valid and internally consistent with provider schemas.

```bash
terraform validate
```

![Terraform Validate](screenshots/session18/task1-3-tf-validate.png)

---

## Task 2: Infrastructure Execution Planning

### 1. Generate Speculative Execution Plan (terraform plan)
Create an execution plan to preview infrastructure modifications (create, update, destroy) against state before committing changes.

```bash
terraform plan
```

![Terraform Plan](screenshots/session18/task2-1-tf-plan.png)

---

## Task 3: Infrastructure Provisioning Lifecycle

### 1. Provision Cloud Resources (terraform apply)
Execute the actions proposed in the Terraform plan to provision cloud infrastructure declaratively.

```bash
terraform apply -auto-approve
```

![Terraform Apply](screenshots/session18/task3-1-tf-apply.png)

---

## Task 4: State Inspection & Outputs Query

### 1. Inspect Current State (terraform show)
Inspect current infrastructure state and attribute mappings tracked within `terraform.tfstate`.

```bash
terraform show
```

![Terraform Show](screenshots/session18/task4-1-tf-show.png)

### 2. Query Output Values (terraform output)
Extract computed resource attributes (bucket name, ARN, region) exported by the configuration.

```bash
terraform output
```

![Terraform Output](screenshots/session18/task4-2-tf-output.png)

---

## Task 5: State Teardown & Resource Decommissioning

### 1. Decommission Managed Infrastructure (terraform destroy)
Destroy all remote infrastructure managed by this Terraform configuration safely and cleanly.

```bash
terraform destroy -auto-approve
```

![Terraform Destroy](screenshots/session18/task5-1-tf-destroy.png)