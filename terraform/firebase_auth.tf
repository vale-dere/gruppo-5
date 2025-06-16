#firebase authentication

resource "google_identity_platform_project_default_config" "default" {
  project = var.project_id

  sign_in {
    google {
      enabled        = true
      client_id      = "IL_TUO_CLIENT_ID"
      client_secret  = "IL_TUO_CLIENT_SECRET"
    }
  }

  authorized_domains = [
    "localhost",
    "${var.project_id}.web.app",
    "${var.project_id}.firebaseapp.com"
  ]
}

/* NOTE
1- Devi creare le credenziali OAuth 2.0 su console.developers.google.com → "OAuth 2.0 Client ID"
2- Incolli client_id e client_secret nei campi qui sopra
3- I domini autorizzati devono includere dove gira la tua app (anche localhost per testing)
*/