```markdown
# ⛵ Sentiment Application Helm Chart

An enterprise-grade, parametrized template manifest system designed to package and deploy our multi-tiered distributed analysis stack with complete configuration flexibility.

## 🎛️ Configurations Matrix

This chart exposes an abstracted configuration model across `values.yaml` (Dev/Global defaults) and `values-prod.yaml` (Production profiles).

| Property | Description | Dev Default | Prod Override |
| :--- | :--- | :--- | :--- |
| `global.environment` | Context flag injected into app runtimes | `dev` | `prod` |
| `gateway.replicaCount`| Horizontally scales routing API targets | `2` | `3` |
| `job.replicaCount` | Horizontally scales state manager pods | `1` | `2` |
| `postgres.password` | Master administrative password key | `supersecretpassword` | `an-actual-secure-prod-password` |
| `ingress.host` | Domain mapping evaluated by the Ingress layer | `localhost` | `api.sentiment.local` |

---

## 🧪 Local Rendering Validation

You can compile and dry-run lint the outputted raw Kubernetes manifests locally without running a live deployment using:

```bash
# Validate Dev output
helm template test-dev-release .

# Validate Production overrides output
helm template test-prod-release . -f values-prod.yaml

```

The dynamic template mechanism automatically formats shared resource pointers (e.g., computing `POSTGRES_HOST` down to `{{ .Release.Name }}-postgres`) which completely guarantees that environments installed side-by-side will never collide.

```