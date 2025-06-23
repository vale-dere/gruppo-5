#!/bin/bash

# Crea un tag unico con data e ora
TAG="v$(date +%Y%m%d-%H%M)"

# Definisci il nome completo dell'immagine con il tag
IMAGE="europe-west1-docker.pkg.dev/gruppo-5/anonimadata-repo/frontend:$TAG"

echo "Building image: $IMAGE"

# Build immagine, con Dockerfile in cartella frontend
docker build -t $IMAGE ./frontend

echo "Pushing image..."
# Push dell'immagine sul Container Registry Artifact Registry
docker push $IMAGE

echo "Updating Terraform file..."
# # Aggiorna il file terraform frontend.tf nella cartella terraform sostituendo la riga con image = "...", 
# facendo attenzione che la sintassi nel .tf corrisponda a questa espressione
sed -i.bak "s|image = \".*\"|image = \"$IMAGE\"|" ./terraform/frontend.tf

echo "Running terraform apply for frontend..."
cd terraform
# Esegui terraform apply per aggiornare il deployment
#terraform apply -auto-approve
terraform apply -var-file="secret_variables.tfvars"
cd ..