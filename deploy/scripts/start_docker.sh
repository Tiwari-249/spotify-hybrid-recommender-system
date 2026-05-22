#!/bin/bash

exec > /home/ubuntu/start_docker.log 2>&1

echo "Logging into ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 458889634556.dkr.ecr.ap-south-1.amazonaws.com

echo "Pulling latest image..."
docker pull 458889634556.dkr.ecr.ap-south-1.amazonaws.com/spotify-recommender-system:latest

echo "Stopping old container..."
docker stop spotify_recommender_system || true

echo "Removing old container..."
docker rm spotify_recommender_system || true

echo "Starting new container..."
docker run -d \
  --restart unless-stopped \
  -p 80:8000 \
  --name spotify_recommender_system \
  458889634556.dkr.ecr.ap-south-1.amazonaws.com/spotify-recommender-system:latest

echo "Deployment completed."