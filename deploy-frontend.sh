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

echo "Updating terraform.tfvars with new image tag..."
# Aggiorna terraform.tfvars invece di backend.tf
sed -i.bak "s|^frontend_image *= *\".*\"|frontend_image = \"$IMAGE\"|" ./terraform/terraform.tfvars

echo "Running terraform apply for frontend..."
cd terraform
# Esegui terraform apply per aggiornare il deployment
#terraform apply -auto-approve
terraform apply -var-file="secret_variables.tfvars"
cd ..