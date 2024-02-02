# R2D AWS Deployment

# CI/CD Pipeline
* The R2D CI/CD Jenkins Pipeline will be deployed in a **t2.MEDIUM EC2**
    * Rationale: SonarQube requires at least 3GB of RAM.
* R2D-ap-southeast-1-Jenkins-dev-001
* Workflow
    1. verify docker, docker compose and git installations
    2. ``git clone https://github.com/Yapping72/R2D.git``
    3. ``cd R2D\jenkins``
    4. ``docker compose build``
    5. ``docker compose up -d``
    6. Configure firewall rules to enable TCP access to ports 8080 and 9000.