resource "google_cloud_run_service" "frontend_service" {
  name     = var.frontend_service_name
  location = var.region

  template {
    spec {
      service_account_name = google_service_account.frontend_sa.email

      containers {
        image = var.frontend_image

        ports {
          container_port = 8080
        }

        env {
          name  = "VITE_FIREBASE_AUTH_DOMAIN"
          value = var.firebase_auth_domain
        }

        env {
          name  = "VITE_FIREBASE_PROJECT_ID"
          value = var.firebase_project_id
        }

        env {
          name  = "VITE_FIREBASE_STORAGE_BUCKET"
          value = var.firebase_storage_bucket
        }

        env {
          name = "VITE_FIREBASE_API_KEY"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.firebase_api_key.secret_id
              key  = "latest"
            }
          }
        }

        env {
          name = "VITE_FIREBASE_MESSAGING_SENDER_ID"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.firebase_messaging_sender_id.secret_id
              key  = "latest"
            }
          }
        }

        env {
          name = "VITE_FIREBASE_APP_ID"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.firebase_app_id.secret_id
              key  = "latest"
            }
          }
        }

        env {
          name = "VITE_API_BASE_URL"
          value_from {
            secret_key_ref {
              name = google_secret_manager_secret.vite_api_base_url.secret_id
              key  = "latest"
            }
          }
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_service_account" "frontend_sa" {
  account_id   = var.frontend_sa_account_id
  display_name = "Service Account per il Frontend Cloud Run"
}


// risorse per variabili
resource "google_secret_manager_secret" "vite_api_base_url" {
  secret_id = "VITE_API_BASE_URL"
  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "vite_api_base_url_version" {
  secret      = google_secret_manager_secret.vite_api_base_url.id
  secret_data_wo = var.vite_api_base_url
}

resource "google_secret_manager_secret" "firebase_api_key" {
  secret_id = "firebase-api-key"
  replication { 
    auto {} 
  }
}

resource "google_secret_manager_secret_version" "firebase_api_key" {
  secret      = google_secret_manager_secret.firebase_api_key.id
  secret_data_wo = var.firebase_api_key
}

resource "google_secret_manager_secret" "firebase_messaging_sender_id" {
  secret_id = "firebase-messaging-sender-id"
  replication { 
    auto {}
  }
}

resource "google_secret_manager_secret_version" "firebase_messaging_sender_id" {
  secret      = google_secret_manager_secret.firebase_messaging_sender_id.id
  secret_data_wo = var.firebase_messaging_sender_id
}

resource "google_secret_manager_secret" "firebase_app_id" {
  secret_id = "firebase-app-id"
  replication { 
    auto {}
  }
}

resource "google_secret_manager_secret_version" "firebase_app_id" {
  secret      = google_secret_manager_secret.firebase_app_id.id
  secret_data_wo = var.firebase_app_id
}