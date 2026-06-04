resource "helm_release" "ingress_nginx" {
  name             = "ingress-nginx"
  repository       = "https://kubernetes.github.io/ingress-nginx"
  chart            = "ingress-nginx"
  version          = "4.10.0"
  namespace        = "ingress-nginx"
  create_namespace = true

  values = [
    <<-EOF
    controller:
      hostPort:
        enabled: true
      # CHANGE HERE: Tell Helm not to look for a Cloud LoadBalancer IP
      service:
        type: NodePort
      nodeSelector:
        ingress-ready: "true"
      tolerations:
        - key: "node-role.kubernetes.io/control-plane"
          operator: "Exists"
          effect: "NoSchedule"
        - key: "node-role.kubernetes.io/master"
          operator: "Exists"
          effect: "NoSchedule"
      publishService:
        enabled: false
      extraArgs:
        publish-status-address: "localhost"
    EOF
  ]

  depends_on = [kind_cluster.this]
}