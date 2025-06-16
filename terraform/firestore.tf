#to use firestore

resource "google_firestore_database" "default" {
  name     = "(default)"
  project  = var.project_id
  location_id = var.region
  type     = "NATIVE"
}