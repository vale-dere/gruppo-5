output "backend_service_url" {
  description = "URL del backend Cloud Run"
  value       = google_cloud_run_service.backend_service.status[0].url
}

output "frontend_service_url" {
  description = "URL del frontend Cloud Run"
  value       = google_cloud_run_service.frontend_service.status[0].url
}