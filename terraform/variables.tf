#variabili sensibili
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



# Variabili pubbliche
variable "firebase_auth_domain" {}
variable "firebase_project_id" {}
variable "firebase_storage_bucket" {}