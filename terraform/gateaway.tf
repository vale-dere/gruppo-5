resource "google_service_account" "gateway_sa" {
  account_id   = "gateway-sa"
  display_name = "Service Account for API Gateway to invoke Cloud Run"
}

resource "google_cloud_run_service_iam_member" "allow_gateway_backend" {
  location = "europe-west1"
  service  = google_cloud_run_service.backend_service.name
  role   = "roles/run.invoker"
  member = "serviceAccount:${google_service_account.gateway_sa.email}"
}

resource "google_project_iam_member" "frontend_can_invoke_gateway" {
  project = "gruppo-5"
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.frontend_sa.email}"
}

resource "google_api_gateway_api" "gateway_api" {
  provider = google-beta
  api_id = "my-backend-api"
}

resource "google_api_gateway_api_config" "gateway_config" {
  provider = google-beta
  api = google_api_gateway_api.gateway_api.api_id
  openapi_documents {
    document {
      path     = "openapi.yaml" 
      contents = filebase64("${path.module}/openapi.yaml")
    }
  }
}


resource "google_api_gateway_gateway" "gateway_instance" {
  provider = google-beta
  gateway_id = "backend-gateway"
  api_config = google_api_gateway_api_config.gateway_config.id
  region = "europe-west1"
}
