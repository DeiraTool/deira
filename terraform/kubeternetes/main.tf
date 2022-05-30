terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.11.0"
    }
  }
}

provider "kubernetes" {
  host = "http://127.0.0.1:8001"
}

resource "kubernetes_deployment" "deira" {
  metadata {
    name = "deira"
  }

  spec {
    selector {
      match_labels = {
        "app" = "deira"
      }
    }
    replicas = 2 

    template {
      metadata {
        labels = {
          "app" = "deira"
        }
      }

      spec {
        container {
          name = "deira"
          image = "hello-world:latest"
          port {
            container_port = 80
          }
        }
      }
    }

  }
}