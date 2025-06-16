#creates a google cloud storage bucket to save csv

resource "google_storage_bucket" "dataset_bucket" {
  name     = "${var.project_id}-datasets"
  location = var.region
  uniform_bucket_level_access = true
}