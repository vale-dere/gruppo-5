resource "google_cloud_run_service" "backend_service" {
  name     = var.backend_service_name
  location = var.region

  template {
    spec {
      containers {
        image = var.backend_image
        ports {
          container_port = 8080
        }
      }
      service_account_name = google_service_account.backend_sa.email
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

# Backend service account (principalmente per chiave json firebase)
resource "google_service_account" "backend_sa" {
  account_id   = var.backend_sa_account_id
  display_name = "Cloud Run Service Account for Backend"
}

