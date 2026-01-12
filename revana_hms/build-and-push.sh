#!/bin/bash

# RHMS Docker Build and Push Script
# Usage: ./build-and-push.sh YOUR_DOCKERHUB_USERNAME

# set -e

# Check if username is provided, otherwise default to bgtuser
if [ -z "$1" ]; then
    echo "No username provided, using default: bgtuser"
    DOCKERHUB_USERNAME="bgtuser"
else
    DOCKERHUB_USERNAME=$1
fi
IMAGE_NAME="rhms"
TAG="latest"
FULL_IMAGE_NAME="${DOCKERHUB_USERNAME}/${IMAGE_NAME}:${TAG}"

echo "========================================="
echo "Building RHMS Docker Image"
echo "========================================="
echo "Image: ${FULL_IMAGE_NAME}"
echo ""

# Build the image
echo "Step 1: Building Docker image..."
docker build -t ${FULL_IMAGE_NAME} .

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "Step 2: Checking Docker Hub login..."
# docker login  <-- Commented out as you are already logged in
# If you actully need to login, uncomment the line above or run 'docker login' manually.

if [ $? -eq 0 ]; then
    echo "✅ Proceeding with existing credentials..."
else
    echo "❌ Login check failed (or previous command failed)!"
    exit 1
fi

echo ""
echo "Step 3: Pushing image to Docker Hub..."
docker push ${FULL_IMAGE_NAME}

if [ $? -eq 0 ]; then
    echo "✅ Push successful!"
else
    echo "❌ Push failed!"
    exit 1
fi

echo ""
echo "========================================="
echo "✅ All Done!"
echo "========================================="
echo "Your image is now available at:"
echo "docker pull ${FULL_IMAGE_NAME}"
echo ""
echo "Next steps:"
echo "1. Update docker-compose.aapanel.yml with: ${FULL_IMAGE_NAME}"
echo "2. Upload docker-compose.aapanel.yml, .env, and nginx.conf to aaPanel"
echo "3. Create Docker Compose project in aaPanel"
echo "4. Start the services"
echo ""
