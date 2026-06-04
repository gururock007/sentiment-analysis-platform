# Sentiment System - API Gateway

The **Gateway** acts as the singular entry point for the distributed sentiment analysis system. It abstracts the core machine learning worker mechanics away from users, handling incoming HTTP traffic, parsing and validating incoming payloads, and preparing unique jobs for asynchronous queuing.

## 📁 Repository Map

```text
.
├── api                     # API layer configuration
│   └── v1
│       ├── endpoints.py    # Route logic handlers for validation & dispatch
│       └── router.py       # Core aggregation hub for API routes
├── core                    # System architecture kernel
│   ├── config.py           # Global settings management and env configurations
│   └── schemas.py          # Strict Pydantic interface validation models
├── main.py                 # Application bootstrapper and ASGI initialization
├── pyproject.toml          # Package architecture & shortcut definitions
└── README.md               # Infrastructure documentation

```

---

## 🛠️ API Architecture Specification

The Gateway exposes two principal endpoints engineered to transition data workloads cleanly out of synchronous execution flows.

### 1. Ingest Data For Analysis

* **Endpoint:** `POST /api/v1/analyze`
* **State:** Asynchronous Ingestion (`22_ACCEPTED`)
* **Payload Blueprint:**

```json
    {
      "text": "The performance of the pipeline was exceptional."
    }
    ```
*   **Response Blueprint:**
```json
    {
      "job_id": "89b703e4-c5a4-436d-8b63-0d588523ef6a",
      "status": "queued"
    }
    ```

### 2. Fetch Job Resolution State
*   **Endpoint:** `GET /api/v1/result/{job_id}`
*   **State:** Polling Entrypoint (`200_OK`)
*   **Response Blueprint (In-Flight):**
```json
    {
      "job_id": "89b703e4-c5a4-436d-8b63-0d588523ef6a",
      "status": "processing"
    }
    ```

---

## 🚀 Deployment & Operational Controls

Ensure your local machine environment has Python 3.10+ installed and activated.

### 1. Installation Environment Sync
Generate the dedicated isolated runtime environment and pull project dependencies securely by running:
```bash
poetry install

```

### 2. Launch Local Hot-Reload Server

Run the local development engine instance bound to your system network interfaces (`0.0.0.0:8000`). Hot-reloading activates automatically whenever system file updates are detected:

```bash
poetry run start

```

### 3. Interactive Open-API Validation Sandbox

Once your server process is active, point your browser destination folder to:

* **Swagger Documentation Sandbox:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* **Alternative Redoc Layout:** [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)
