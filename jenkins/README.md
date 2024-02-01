# Docker Containers
The [docker-compose.yml](docker-compose.yml) will create 3 containers - Jenkins, SonarQube and PostgresSQL DB.
* Jenkins is built using a custom Dockerfile that installs docker, docker-compose, docker cli and 3 jenkins plugins - BlueOcean, OWASP Dependency Checks and SonarQube Scanner.
* Jenkins image will also contain Chrome and Selenium libraries to enable UI testing with selenium. 
* See below on  how to configure the Jenkins Plugins

## Usage
1. Navigate to [setup-jenkins directory](setup-jenkins\README.md)
2. ``docker-compose build``
3. ``docker-compose up -d``
4. Verify containers are up
    * ``docker ps``
5. Access via:
    * **Jenkins**: ``http:localhost:8080`` 
    * **SonarQube**: ``http:localhost:9000``
6. The pipeline will run OWASP dependency checks, SonarQube, Build and start docker images and run UI Tests.

## Setting Jenkins with OWASP Dependency Checks and SonarQube
1. Dockerfile will build a Jenkins image with the following plugins:
    * BlueOcean Plugin
    * OWASP Dependency Check
    * SonarQube Scanner
2. To configure OWASP Dependency Check:
    *  Manage Jenkins > Tool Configuration > Add Dependency Check > Install Automatically > Add installer automatically and select the git version.
3. Setting up SonarQube:
    * Follow X09 SonarQube Lab.
    * Login using admin/admin.
    * Create project manually > name your project **OWASP** with Project Key **OWASP** > Use Global Settings > Locally > Generate a Token for the OWASP project.
    * SonarQube is now configured. You can integrate SonarQube with Jenkins using the SonarQube Scanner.
4. Integrating SonarQube with SonarQube Scanner.
    * Manage Jenkins > System Configuration > Add SonarQube > Add authentication token as secret text (the token u generated for OWASP project). 
    * Tool Configuration > SonarQube Scanner > Add SonarQube Scanner and name it **SonarQube** > Install automatically (from Maven Central).