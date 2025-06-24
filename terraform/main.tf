#entry point

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = ">= 6.0.0"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = ">= 6.0.0"
    }
  }
}

// da valutare creazione file providers 

provider "google" { 
  project = "gruppo-5" 
  region  = "europe-west1"
}

provider "google-beta" {
  project = "gruppo-5"
  region  = "europe-west1"
}

