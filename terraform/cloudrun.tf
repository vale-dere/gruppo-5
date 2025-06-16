#defines frontend and backend

resource "google_cloud_run_service" "backend" {
  name     = "anonimadata-backend"
  location = var.region

  template {
    spec {
      containers {
        image = "gcr.io/${var.project_id}/anonimadata-backend:latest"
        ports {
          container_port = 8080
        }
        env {
          name  = "BUCKET_NAME"
          value = google_storage_bucket.dataset_bucket.name
        }
      }
    }
  }

  traffics {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service" "frontend" {
  name     = "anonimadata-frontend"
  location = var.region

  template {
    spec {
      containers {
        image = var.frontend_image
        ports {
          container_port = 80
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

//questo blocco sotto non serve, perchè configura l'accesso pubblico alla risorsa e noi dobbiamo autenticarlo con firebase da traccia.
// per ora lo lascio commentato giusto perchè non siamo pratiche e potremmo averne bisogno come memo. Lo elimineremo più in là
/*
resource "google_cloud_run_service_iam_member" "allow_all" {
  location = google_cloud_run_service.backend.location
  service  = google_cloud_run_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
} */ 
