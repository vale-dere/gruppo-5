resource "google_project_service" "firestore" {
  service = "firestore.googleapis.com"
}

resource "google_firestore_database" "default" {
  name        = "(default)"
  project     = "gruppo-5"
  location_id = "europe-west1"
  type        = "FIRESTORE_NATIVE"
}
