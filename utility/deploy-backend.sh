#!/bin/bash

# Tag unico con data e ora
TAG="v$(date +%Y%m%d-%H%M)"

# Nome immagine completa con tag
IMAGE="europe-west1-docker.pkg.dev/gruppo-5/anonimadata-repo/backend:$TAG"

echo "Building backend image: $IMAGE"

# Build immagine, con Dockerfile in cartella backend
docker build -t $IMAGE ./backend

echo "Pushing backend image..."
docker push $IMAGE

echo "Updating terraform.tfvars with new image tag..."
# Aggiorna terraform.tfvars invece di backend.tf
sed -i.bak "s|^backend_image *= *\".*\"|backend_image = \"$IMAGE\"|" ./terraform/terraform.tfvars

echo "Running terraform apply for backend..."
cd terraform
#terraform apply -auto-approve
terraform apply -var-file="secret_variables.tfvars"
cd ..