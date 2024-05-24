#!/bin/bash
# Update all packages
sudo yum update -y

#Install Docker
sudo yum install -y docker
sudo service docker start

# Start Docker and enable it to start on boot
service docker start
systemctl enable docker

sudo yum install git -y

# Add ec2-user to the Docker group
usermod -a -G docker ec2-user

# Install Docker Compose V2
# Replace with the latest version if necessary
DOCKER_COMPOSE_VERSION="v2.20.2"
mkdir -p /usr/local/lib/docker/cli-plugins
curl -SL "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-linux-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
chmod +x /usr/local/lib/docker/cli-plugins/docker-compose

# Set timezone to Singapore
timedatectl set-timezone Asia/Singapore
