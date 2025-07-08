resource "google_storage_bucket" "datasets_bucket" {
  name                        = "gruppo5-datasets"      
  location                    = "EUROPE-WEST1"
  force_destroy               = true                   # Per eliminare bucket anche se non vuoto (comodo per test)
  uniform_bucket_level_access = true                   # Consigliato per sicurezza e semplicità

  cors {
    origin          = ["https://frontend-service-583549727222.europe-west1.run.app"]
    method          = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS"]
    response_header = ["Content-Type", "Content-Disposition"]
    max_age_seconds = 3600
  }
}