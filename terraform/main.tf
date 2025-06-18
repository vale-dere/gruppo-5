#entry point
/*
module "storage" {
  source = "./storage"
}

module "cloudrun" {
  source         = "./cloudrun"
  backend_image  = var.backend_image
  frontend_image = var.frontend_image
  project_id     = var.project_id
  region         = var.region
}
*/

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" { #non è stato creato un file providers apposito utlizzando solo google ed essendo un tema di sole 2 persone
  project = "gruppo-5" 
  region  = "europe-west1"
}



