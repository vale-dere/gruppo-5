# === Variabili sensibili ===
variable "vite_api_base_url" {
  description = "Backend URL (esposto come env var)"
  type        = string
  sensitive   = true
}
variable "firebase_api_key" {
  sensitive = true
}
variable "firebase_messaging_sender_id" {
  sensitive = true
}
variable "firebase_app_id" {
  sensitive = true
}



# === Variabili pubbliche ===
variable "firebase_auth_domain" {}
variable "firebase_project_id" {}
variable "firebase_storage_bucket" {}
variable "region" {
  description = "Regione di deploy"
  type        = string
}
variable "project_id" {
  description = "Id progetto"
  type        = string
}

# === Backend ===
variable "backend_service_name" {
  description = "Nome del servizio Cloud Run backend"
  type        = string
}

variable "backend_image" {
  description = "Immagine container backend"
  type        = string
}

variable "backend_sa_account_id" {
  description = "ID della service account per il backend"
  type        = string
}

# === Frontend ===
variable "frontend_service_name" {
  description = "Nome del servizio Cloud Run frontend"
  type        = string
}

variable "frontend_image" {
  description = "Immagine container frontend (con tag)"
  type        = string
}

variable "frontend_sa_account_id" {
  description = "ID della service account per il frontend"
  type        = string
}