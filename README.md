# Dockerized Node.js & Flask Application

This project consists of a Node.js/Express frontend and a Flask backend, containerized using Docker.

## Docker Images

You can pull the pre-built images from Docker Hub:

### Frontend
```bash
docker pull sudarshan09/frontend-app:latest
```

### Backend
```bash
docker pull sudarshan09/backend-app:latest
```

## Running the Application

To run the application using Docker Compose:

```bash
docker-compose up
```

The frontend will be available at `http://localhost:3000`.

## Project Structure

- **frontend**: Node.js Express application serving a contact form.
- **backend**: Flask application processing form submissions.

# CI/CD Deployment on EC2 with Jenkins

This section covers deploying Flask and Express apps on a single EC2 instance and automating the process with Jenkins.

## Prerequisites
- AWS Account
- GitHub Repository: [https://github.com/NaruSudarshan/devops_project](https://github.com/NaruSudarshan/devops_project)

## Part 1: EC2 Setup (Manual)

1.  **Launch EC2 Instance**:
    - **OS**: Ubuntu Server 22.04 LTS
    - **Type**: t2.micro (Free Tier)
    - **Security Group**: Allow SSH (22), HTTP (80), Custom TCP (3000), Custom TCP (5000), Custom TCP (8080).

2.  **Install Dependencies**:
    SSH into your instance and run:
    ```bash
    sudo apt update
    sudo apt install -y python3-pip nodejs npm git openjdk-21-jdk
    sudo npm install -g pm2
    ```

3.  **Install Jenkins**:
    ```bash
    curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
    echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/ | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
    sudo apt update
    sudo apt install -y jenkins
    sudo systemctl start jenkins
    ```
    - Unlock Jenkins using the password from `/var/lib/jenkins/secrets/initialAdminPassword`.

## Part 2: Jenkins Freestyle Setup

1.  **Create Backend Job**:
    - **Type**: Freestyle project
    - **Source**: Git (URL: `https://github.com/NaruSudarshan/devops_project`)
    - **Branch**: `*/main`
    - **Triggers**: GitHub hook trigger for GITScm polling
    - **Build Steps (Execute Shell)**:
      ```bash
      export PATH=$PATH:/usr/local/bin
      cd backend
      pip3 install -r requirements.txt --break-system-packages
      pm2 restart flask-backend || pm2 start app.py --name flask-backend --interpreter python3
      ```

2.  **Create Frontend Job**:
    - **Type**: Freestyle project
    - **Source**: Git (URL: `https://github.com/NaruSudarshan/devops_project`)
    - **Branch**: `*/main`
    - **Triggers**: GitHub hook trigger for GITScm polling
    - **Build Steps (Execute Shell)**:
      ```bash
      export PATH=$PATH:/usr/local/bin
      cd frontend
      npm install
      pm2 restart express-frontend || pm2 start server.js --name express-frontend
      ```

3.  **Configure Webhook**:
    - In GitHub Repo > Settings > Webhooks.
    - URL: `http://your-ec2-ip:8080/github-webhook/`
    - Content type: `application/json`

## Screenshots

### Running EC2 Instance
![EC2 Instance](./screenshots/ec2_instance.png)

### Jenkins Dashboard
![Jenkins Dashboard](./screenshots/jenkins_dashboard.png)

### Successful Build Status
![Backend Build](./screenshots/backend_build.png)
![Frontend Build](./screenshots/frontend_build.png)

## Jenkins Pipeline Execution Logs

### Frontend Build Log
```text
Started by user admin
Running as SYSTEM
Building in workspace /var/lib/jenkins/workspace/Frontend-Freestyle
...
[Frontend-Freestyle] $ /bin/sh -xe /tmp/jenkins5725865414022831128.sh
+ export PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/snap/bin:/usr/bin:/usr/local/bin
+ cd frontend
+ npm install
added 76 packages, and audited 77 packages in 2s
...
+ pm2 start server.js --name express-frontend
[PM2] Starting /var/lib/jenkins/workspace/Frontend-Freestyle/frontend/server.js in fork_mode (1 instance)
[PM2] Done.
Finished: SUCCESS
```

### Backend Build Log
```text
Started by user admin
Running as SYSTEM
Building in workspace /var/lib/jenkins/workspace/Backend-Freestyle
...
[Backend-Freestyle] $ /bin/sh -xe /tmp/jenkins14054670491969934317.sh
+ cd backend
+ pip3 install -r requirements.txt --break-system-packages
...
Successfully installed Flask-3.0.0 Werkzeug-3.1.3 flask-cors-4.0.0 itsdangerous-2.2.0
+ pm2 restart flask-backend
...
+ pm2 start app.py --name flask-backend --interpreter python3
[PM2] Starting /var/lib/jenkins/workspace/Backend-Freestyle/backend/app.py in fork_mode (1 instance)
[PM2] Done.
Finished: SUCCESS
```

