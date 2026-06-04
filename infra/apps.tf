# Deploy Dev Release
resource "helm_release" "dev_release" {
  name             = "dev-release"
  chart            = "${path.module}/../deployment/charts/sentiment-app"
  namespace        = "sentiment-dev"
  create_namespace = true

  # Uses the default values.yaml found inside your chart directory
  depends_on = [helm_release.ingress_nginx]
}

# Deploy Prod Release 
resource "helm_release" "prod_release" {
  name             = "prod-release"
  chart            = "${path.module}/../deployment/charts/sentiment-app"
  namespace        = "sentiment-prod"
  create_namespace = true

  # Override with your production specific properties
  values = [
    file("${path.module}/../deployment/charts/sentiment-app/values-prod.yaml")
  ]

  depends_on = [helm_release.ingress_nginx]
}