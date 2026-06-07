```markdown
# 🚀 End-to-End Distributed Sentiment Analysis Stack

A production-ready, highly-scalable asynchronous machine learning inference stack. This project utilizes a microservice architecture to ingest text data, queue background NLP inference tasks, and serve predictions across dynamically isolated Dev and Prod environments.

The entire infrastructure—from the local Kubernetes cluster to the Ingress controllers and application releases—is provisioned deterministically using **Terraform** and **Helm**.

---

## 🏗️ Architecture Overview

```text
[ Client Request ] 
       │
       ▼ (Port 8080)
┌────────────────────────────────────────────────────────┐
│                   Nginx Ingress                        │
└────────────────────────────────────────────────────────┘
       │                              │
       ├─► / (Default)                ├─► /job-service/*
       ▼                              ▼
┌──────────────┐               ┌──────────────┐
│   Gateway    │               │ Job Service  │
│  (FastAPI)   │               │  (FastAPI)   │
└──────────────┘               └──────────────┘
                                      │
                                      ▼ (Saves State)
                               ┌──────────────┐      ┌──────────────┐
                               │  PostgreSQL  │ ◄──► │ Redis Queue  │
                               └──────────────┘      └──────────────┘
                                                            ▲
                                                            │ (Pulls Tasks)
                                                     ┌──────────────┐
                                                     │ Worker Pods  │
                                                     │  (Scikit)    │
                                                     └──────────────┘

```

### Microservices

* **`gateway-service`**: Ultra-fast routing layer built with FastAPI to handle front-facing public requests.
* **`job-service`**: State manager that tracks asynchronous pipeline jobs, writes transactions to PostgreSQL, and pushes execution tasks to Redis.
* **`worker-service`**: Decoupled background task processors that ingest NLP payloads, run model inference (`Scikit-Learn`), and update task states.

---

## 🛠️ Tech Stack & Tooling

* **Language/Runtime:** Python 3.14 + `uv` (Fast package manager)
* **Infrastructure:** Terraform (IaC), Kind (Kubernetes-in-Docker)
* **Package Management:** Helm v3 (Kubernetes Templating)
* **Ingress Controller:** Nginx Ingress
* **Datastores:** PostgreSQL 15, Redis 7

---

## ⚡ Quick Start (The One-Command Loop)

The entire architecture is fully automated via a local `Makefile`.

### Prerequisites

Ensure you have the following installed locally:

* Docker Desktop
* Terraform (>= 1.0.0)
* Kind
* Kubectl

### Spin Up Everything

Run the following command from the root directory. This compiles the Python apps, builds the Docker images, loads them into the cluster nodes, and triggers `terraform apply`:

```bash
make

```

### Verify Routing Environments

The cluster automatically binds to your local network via HostPorts.

```bash
# Test the Dev Environment Gateway
curl http://localhost:8080/

# Test the Production Environment Gateway (Routed via Host Header)
curl -H "Host: api.sentiment.local" http://localhost:8080/

### Tear Down Everything

Wipe the entire cluster, network resources, and local resources cleanly:

```bash
make destroy
```
```