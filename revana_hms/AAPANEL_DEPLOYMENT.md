# aaPanel Docker Deployment Guide

This guide will help you deploy RHMS on aaPanel using Docker.

## Step 1: Build and Push Docker Image

### 1.1 Login to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password
```

### 1.2 Build the Image
```bash
cd /home/bhavan/Desktop/RHMS/revana_hms

# Build with your Docker Hub username
docker build -t YOUR_DOCKERHUB_USERNAME/rhms:latest .

# Example: docker build -t johndoe/rhms:latest .
```

### 1.3 Push to Docker Hub
```bash
docker push YOUR_DOCKERHUB_USERNAME/rhms:latest
```

## Step 2: Prepare Files for aaPanel

You'll need to upload these files to your aaPanel server:
1. `docker-compose.aapanel.yml` (renamed docker-compose file)
2. `.env` (environment variables)
3. `nginx.conf` (nginx configuration)

## Step 3: Deploy on aaPanel

### 3.1 Access aaPanel Docker Manager
1. Login to aaPanel
2. Go to **Docker** → **Compose**
3. Click **Add Project**

### 3.2 Create New Project
- **Project Name**: `rhms`
- **Template**: Upload `docker-compose.aapanel.yml`
- Click **Submit**

### 3.3 Configure Environment
1. In the project settings, add environment variables from `.env` file
2. Or upload `.env` file to the project directory

### 3.4 Start Services
1. Click **Start** button
2. Wait for all containers to be healthy
3. Check logs if any issues

### 3.5 Initial Setup
Access the web container terminal in aaPanel and run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## Step 4: Access Your Application

- **Application**: http://YOUR_SERVER_IP
- **Admin Panel**: http://YOUR_SERVER_IP/admin

## Troubleshooting

### Check Container Logs
In aaPanel Docker Manager:
1. Select your project
2. Click on container name
3. View logs

### Restart Services
1. Select project
2. Click **Restart**

### Update Application
```bash
# Pull new image
docker pull YOUR_DOCKERHUB_USERNAME/rhms:latest

# Restart in aaPanel
```

## Important Notes

1. **Database Persistence**: Data is stored in Docker volumes managed by aaPanel
2. **Backups**: Use aaPanel's backup features for database and volumes
3. **SSL**: Configure SSL through aaPanel's website management
4. **Firewall**: Ensure ports 80 and 443 are open in aaPanel security settings
