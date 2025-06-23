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

echo "Updating backend.tf image tag..."
# Aggiorna il file terraform backend.tf nella cartella terraform
sed -i.bak "s|image = \".*\"|image = \"$IMAGE\"|" ./terraform/backend.tf

echo "Running terraform apply for backend..."
cd terraform
#terraform apply -auto-approve
terraform apply -var-file="secret_variables.tfvars"
cd ..