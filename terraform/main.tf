#entry point

module "storage" {
  source = "./storage"
}

module "cloudrun" {
  source         = "./cloudrun"
  backend_image  = var.backend_image
  frontend_image = var.frontend_image
  project_id     = var.project_id
  region         = var.region
}