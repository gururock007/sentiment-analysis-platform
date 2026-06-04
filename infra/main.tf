resource "kind_cluster" "this" {
  name            = "sentiment-cluster"
  kubeconfig_path = pathexpand("~/.kube/config")
  wait_for_ready  = true

  kind_config {
    kind        = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
      kubeadm_config_patches = [
        <<-EOF
        kind: InitConfiguration
        nodeRegistration:
          kubeletExtraArgs:
            node-labels: "ingress-ready=true"
        EOF
      ]

      # Map local port 8080 to container port 80 (HTTP)
      extra_port_mappings {
        container_port = 80
        host_port      = 8080
        listen_address = "0.0.0.0"
      }

      # Map local port 8443 to container port 443 (HTTPS)
      extra_port_mappings {
        container_port = 443
        host_port      = 8443
        listen_address = "0.0.0.0"
      }
    }
  }
}