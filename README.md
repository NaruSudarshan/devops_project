# DevOps Project: Node.js Frontend + Flask Backend

This is a simple web application with a Node.js/Express frontend and a Python/Flask backend. The frontend serves a contact form, and the backend handles the form submissions.

I've containerized both services using Docker and set up a CI/CD pipeline using Jenkins on an AWS EC2 instance.

## Quick Start (Docker)

If you want to run this locally, you can use the pre-built images from Docker Hub.

1.  **Pull the images:**
    ```bash
    docker pull sudarshan09/frontend-app:latest
    docker pull sudarshan09/backend-app:latest
    ```

2.  **Run with Docker Compose:**
    ```bash
    docker-compose up
    ```
    The frontend will be running at `http://localhost:3000`.

## Project Structure

*   `frontend/`: Node.js Express app (serves the UI).
*   `backend/`: Flask app (API for form handling).
*   `docker-compose.yaml`: Orchestrates the two services.

---

## Deployment & CI/CD Setup

I deployed this on a single AWS EC2 instance (Ubuntu 22.04) and used Jenkins to automate the deployment process. Here's a breakdown of the setup.

### 1. Server Setup (EC2)
I used a `t2.micro` instance with Ubuntu 22.04.
*   **Ports Opened:** 22 (SSH), 80 (HTTP), 3000 (Frontend), 5000 (Backend), 8080 (Jenkins).
*   **Dependencies Installed:**
    *   Java (OpenJDK 21) for Jenkins.
    *   Node.js & npm for the frontend.
    *   Python3 & pip for the backend.
    *   `pm2` (globally installed) to keep the apps running in the background.

### 2. Jenkins Configuration
I set up Jenkins on port 8080 and created two "Freestyle" projects to handle the deployments.

*   **Backend Job:**
    *   Pulls code from the `main` branch.
    *   Installs Python requirements (using `--break-system-packages` for Ubuntu 24.04 compatibility).
    *   Restarts the Flask app using `pm2`.

*   **Frontend Job:**
    *   Pulls code from the `main` branch.
    *   Installs npm packages.
    *   Restarts the Express app using `pm2`.

Both jobs are triggered automatically by a **GitHub Webhook** whenever I push code to the repository.

## Screenshots

### Live Application (EC2)
![EC2 Instance](./screenshots/ec2_instance.png)

### Jenkins Dashboard
![Jenkins Dashboard](./screenshots/jenkins_dashboard.png)

### Build Logs
**Backend Build:**
![Backend Build](./screenshots/backend_build.png)

**Frontend Build:**
![Frontend Build](./screenshots/frontend_build.png)

## Logs

Here are snippets from the latest successful build logs:

**Frontend:**
```text
Started on Nov 25, 2025, 11:31:10 AM
Started by event from 140.82.115.12 ⇒ http://3.110.174.105:8080/github-webhook/ on Tue Nov 25 11:31:10 UTC 2025
Using strategy: Default
[poll] Last Built Revision: Revision 5d85ffdb6203f3280c0d2274ed6f1ee990c73e09 (refs/remotes/origin/main)
The recommended git tool is: NONE
No credentials specified
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git ls-remote -h -- https://github.com/NaruSudarshan/devops_project # timeout=10
Found 1 remote heads on https://github.com/NaruSudarshan/devops_project
[poll] Latest remote head revision on refs/heads/main is: aa358898d714f0f2a918ffbe9ccaa30d8c587a61
Done. Took 0.9 sec
Changes found
```

**Backend:**
```text
Started on Nov 25, 2025, 11:31:10 AM
Started by event from 140.82.115.12 ⇒ http://3.110.174.105:8080/github-webhook/ on Tue Nov 25 11:31:10 UTC 2025
Using strategy: Default
[poll] Last Built Revision: Revision 5d85ffdb6203f3280c0d2274ed6f1ee990c73e09 (refs/remotes/origin/main)
The recommended git tool is: NONE
No credentials specified
 > git --version # timeout=10
 > git --version # 'git version 2.43.0'
 > git ls-remote -h -- https://github.com/NaruSudarshan/devops_project # timeout=10
Found 1 remote heads on https://github.com/NaruSudarshan/devops_project
[poll] Latest remote head revision on refs/heads/main is: aa358898d714f0f2a918ffbe9ccaa30d8c587a61
Done. Took 0.9 sec
Changes found
```
