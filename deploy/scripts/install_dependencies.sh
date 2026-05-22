#!/bin/bash

# Exit immediately if a command exits with non-zero status
set -e

# Non-interactive mode
export DEBIAN_FRONTEND=noninteractive

echo "Updating packages..."
sudo apt-get update -y

echo "Installing Docker..."
sudo apt-get install -y docker.io

echo "Starting Docker service..."
sudo systemctl start docker
sudo systemctl enable docker

echo "Installing utilities..."
sudo apt-get install -y unzip curl

echo "Installing AWS CLI v2..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/home/ubuntu/awscliv2.zip"

unzip -o /home/ubuntu/awscliv2.zip -d /home/ubuntu/

sudo /home/ubuntu/aws/install --update

echo "Adding ubuntu user to docker group..."
sudo usermod -aG docker ubuntu

echo "Cleaning installation files..."
rm -rf /home/ubuntu/awscliv2.zip /home/ubuntu/aws

echo "Dependencies installed successfully."