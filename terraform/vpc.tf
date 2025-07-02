module "vpc-module" {
  source       = "terraform-google-modules/network/google"
  version      = "~> 10.0"
  project_id   = "gruppo-5" 
  network_name = "anonimadata-vpc-network"
  mtu          = 1460

  subnets = [
    {
      subnet_name           = "private-subnet-01"
      subnet_ip             = "10.0.1.0/24"
      subnet_region         = "europe-west1"
      subnet_private_access = true  # permette ai VM e servizi nella subnet di accedere a servizi Google privati (senza internet)
      subnet_flow_logs      = false # disabilitato, puoi abilitare se vuoi
    }
  ]
}

resource "google_vpc_access_connector" "cloud_run_connector" {
  name   = "cloud-run-connector"
  region = "europe-west1"
  network = module.vpc-module.network_name
  ip_cidr_range = "10.8.0.0/28" # range IP per il connettore VPC (non deve sovrapporsi con subnet)
  min_instances = 2
  max_instances = 10
}

# Firewall: permette traffico interno nella VPC
resource "google_compute_firewall" "rules" {
  name        = "anonimadata-firewall-rule"
  network     = module.vpc-module.network_name
  description = "Creates firewall rule targeting tagged instances"

  allow {
    protocol = "all" #se funziona aumentiamo granularità
    /*
    protocol = "tcp"
    ports    = ["80", "443"]
    */
  }

  source_ranges = ["10.0.1.0/24"]
  direction     = "INGRESS"
  priority      = 1000
}