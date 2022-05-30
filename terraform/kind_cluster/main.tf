terraform {
  required_providers {
    kind = {
      source = "kyma-incubator/kind"
      version = "0.0.11"
    }
  }
}

provider "kind" {}

resource "kind_cluster" "default" {

  name = "test-cluster"
  wait_for_ready = true

  kind_config {
    kind = "Cluster"
    api_version = "kind.x-k8s.io/v1alpha4"

    node {
      role = "control-plane"
      image = "kindest/node:v1.24.1"

      extra_port_mappings {
        container_port = 80
        host_port = 80
      }

      extra_port_mappings {
        container_port = 443
        host_port = 443
      }
    }

    node {
      role = "worker"
      image = "kindest/node:v1.24.1"
    }

    node {
      role = "worker"
      image = "kindest/node:v1.24.1"
    }

    node {
      role = "worker"
      image = "kindest/node:v1.24.1"
    }
    
  }
}