# Docker Deployment Guide for RHMS

This guide will help you deploy the Revana Hospital Management System using Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Get Docker Compose](https://docs.docker.com/compose/install/))

## Quick Start

### 1. Environment Setup

Make sure your `.env` file has the correct database configuration:

```env
DB_NAME=rhms_db
DB_USER=rhms_user
DB_PASSWORD=your_secure_password
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=your_root_password

SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

DEFAULT_FROM_EMAIL=your-email@example.com
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 2. Build and Run

```bash
# Build the Docker images
docker-compose build

# Start all services
docker-compose up -d

# Check if containers are running
docker-compose ps
```

### 3. Initial Setup

```bash
# Create superuser
docker-compose exec web python manage.py createsuperuser

# Check logs
docker-compose logs -f web
```

### 4. Access the Application

- **Application**: http://localhost
- **Admin Panel**: http://localhost/admin
- **API**: http://localhost/api

## Docker Commands

### Start Services
```bash
docker-compose up -d
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f db
docker-compose logs -f nginx
```

### Restart Services
```bash
docker-compose restart
```

### Run Migrations
```bash
docker-compose exec web python manage.py migrate
```

### Collect Static Files
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

### Access Django Shell
```bash
docker-compose exec web python manage.py shell
```

### Database Backup
```bash
docker-compose exec db mysqldump -u rhms_user -p rhms_db > backup.sql
```

### Database Restore
```bash
docker-compose exec -T db mysql -u rhms_user -p rhms_db < backup.sql
```

## Production Deployment

### 1. Update Settings

In `revana_hms/settings.py`, ensure:
- `DEBUG = False`
- `ALLOWED_HOSTS` includes your domain
- `SECURE_SSL_REDIRECT = True` (if using HTTPS)

### 2. Use Production Database

Update `.env` with production database credentials.

### 3. SSL/HTTPS Setup

For HTTPS, update `nginx.conf`:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    # ... rest of configuration
}
```

### 4. Deploy

```bash
docker-compose -f docker-compose.yml up -d --build
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs web
```

### Database connection issues
```bash
# Check if DB is healthy
docker-compose ps

# Restart DB
docker-compose restart db
```

### Permission issues
```bash
# Fix permissions
docker-compose exec web chown -R www-data:www-data /app/media
docker-compose exec web chown -R www-data:www-data /app/staticfiles
```

### Clear everything and start fresh
```bash
docker-compose down -v
docker-compose up -d --build
```

## Scaling

To run multiple web workers:

```bash
docker-compose up -d --scale web=3
```

## Monitoring

### Check resource usage
```bash
docker stats
```

### Check container health
```bash
docker-compose ps
```

## Backup Strategy

1. **Database**: Regular mysqldump backups
2. **Media Files**: Backup `/app/media` volume
3. **Configuration**: Keep `.env` and configs in version control (encrypted)

## Security Checklist

- [ ] Change default passwords in `.env`
- [ ] Set `DEBUG=False` in production
- [ ] Configure firewall rules
- [ ] Enable HTTPS
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor logs for suspicious activity
