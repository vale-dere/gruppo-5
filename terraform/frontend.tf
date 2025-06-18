resource "google_cloud_run_service" "frontend_service" {
  name     = "frontend-service"
  location = "europe-west1"

  template {
    spec {
      containers {
        image = "europe-west1-docker.pkg.dev/gruppo-5/anonimadata-repo/frontend:latest"
        ports {
          container_port = 8080
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}
/*
# IAM binding per frontend (autorizzazioni invoker)
resource "google_cloud_run_service_iam_binding" "frontend_invokers" {
  service  = google_cloud_run_service.frontend_service.name
  location = google_cloud_run_service.frontend_service.location
  role     = "roles/run.invoker"
  members = [
    "user:valentina.derespinis@fidogroup.it",
    "user:danila.meleleo@fidogroup.it",
  ]
}
*/

resource "google_cloud_run_service_iam_member" "frontend_invoker_user1" {
  service  = "frontend-service"
  location = "europe-west1"
  role     = "roles/run.invoker"
  member   = "user:valentina.derespinis@fidogroup.it"
}

resource "google_cloud_run_service_iam_member" "frontend_invoker_user2" {
  service  = "frontend-service"
  location = "europe-west1"
  role     = "roles/run.invoker"
  member   = "user:danila.meleleo@fidogroup.it"
}