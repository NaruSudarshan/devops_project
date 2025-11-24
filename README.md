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
