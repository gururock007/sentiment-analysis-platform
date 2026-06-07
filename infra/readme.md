```markdown
# 🏛️ Infrastructure as Code (IaC) Configuration

This directory contains the Terraform configuration files responsible for orchestrating the lifecycle of the local Kubernetes engine and its core platform dependencies.

## 📋 Resource Blueprint

* **`provider.tf`**: Sets up the decoupled dependency chain. It instantiates the `kind` cluster provider, then dynamically extracts authentication tokens to boot up the `kubernetes` and `helm` providers *on the fly*.
* **`main.tf`**: Defines the `kind_cluster` resource. Customizes the master node topology to match `ingress-ready=true` labels and maps ingress traffic (`80` / `443`) straight to host ports `8080` and `8443`.
* **`ingress.tf`**: provisions the community `ingress-nginx` controller via Helm, bypassing standard cloud provider `LoadBalancer` blockers by utilizing a local `NodePort` mapping.
* **`apps.tf`**: Declares multi-tenant application isolation by spinning up dual Helm tracking modules (`dev-release` and `prod-release`) into completely sandboxed namespaces.

---

## ⚙️ Manual Management

While the root-level `Makefile` is preferred, you can debug or inspect the terraform graph directly within this folder:

```bash
# Initialize providers
terraform init

# Plan variations
terraform plan

# Deploy changes directly
terraform apply -auto-approve

```

> ⚠️ **State Note:** The local terraform tracking state (`terraform.tfstate`) is explicitly ignored by version control to protect localized cluster signatures. Do not commit state files.

```