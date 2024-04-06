FROM jenkins/jenkins:lts
USER root
RUN apt-get update && apt-get install -y lsb-release
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc \
  https://download.docker.com/linux/debian/gpg
RUN echo "deb [arch=$(dpkg --print-architecture) \
  signed-by=/usr/share/keyrings/docker-archive-keyring.asc] \
  https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list
RUN apt-get update && apt-get install -y docker.io
# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/v2.5.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose
# Install dependencies for Chrome
RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    --no-install-recommends
# Add Google Chrome to the repositories
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list
# Install Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends
# Install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
# Install Node.js and npm from node:latest image
RUN apt-get update && apt-get install -y nodejs npm
# Clean up APT caches to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN jenkins-plugin-cli --plugins "dependency-check-jenkins-plugin:5.4.3"
RUN jenkins-plugin-cli --plugins "sonar:2.17.1"
# Switch back to the Jenkins user
USER jenkin