resource "google_cloud_run_service" "backend_service" {
  name     = "backend-service"
  location = "europe-west1"

  template {
    spec {
      containers {
        image = "europe-west1-docker.pkg.dev/gruppo-5/anonimadata-repo/backend:v20250623-1320"
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

/*
# IAM binding per permettere a utenti specifici di invocare backend
resource "google_cloud_run_service_iam_binding" "backend_invokers" {
  service  = google_cloud_run_service.backend_service.name
  location = google_cloud_run_service.backend_service.location
  role     = "roles/run.invoker"
  members = [
    "user:valentina.derespinis@fidogroup.it",
    "user:danila.meleleo@fidogroup.it",
  ]
}
*/

# Backend IAM members
resource "google_cloud_run_service_iam_member" "backend_invoker_user1" {
  service  = "backend-service"
  location = "europe-west1"
  role     = "roles/run.invoker"
  member   = "user:valentina.derespinis@fidogroup.it"
}

resource "google_cloud_run_service_iam_member" "backend_invoker_user2" {
  service  = "backend-service"
  location = "europe-west1"
  role     = "roles/run.invoker"
  member   = "user:danila.meleleo@fidogroup.it"
}

# Backend service account (principalmente per chiave json firebase)
resource "google_service_account" "backend_sa" {
  account_id   = "backend-sa"
  display_name = "Cloud Run Service Account for Backend"
}

