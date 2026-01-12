# Deployment Guide for RHMS

This guide outlines the steps to deploy the RHMS application to a new server using Docker (Recommended) or a manual setup.

## Prerequisites

-   **Server**: A Linux server (Ubuntu 20.04/22.04 recommended).
-   **Domain**: Pointed to your server's IP.
-   **Tools**: Git, Docker, Docker Compose.

## Option 1: Docker Deployment (Recommended)

This allows for a consistent environment identical to development.

### 1. Install Docker & Docker Compose
```bash
# Update and install Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# (Log out and back in for group changes to take effect)
```

### 2. Clone the Repository
```bash
git clone <YOUR_REPOSITORY_URL>
cd revana_hms
```

### 3. Configure Environment
Create a `.env` file in the project root (or copy `.env.example` if available).
```bash
nano .env
```
**Required Variables:**
```ini
DEBUG=False
SECRET_KEY=your-secure-secret-key-here
ALLOWED_HOSTS=yourdomain.com,server-ip

# Database
DB_NAME=revana_hms_db
DB_USER=root
DB_PASSWORD=your_secure_password
DB_HOST=db  # Hostname is service name in docker-compose
DB_PORT=3306
```

### 4. Build and Run
```bash
docker-compose up -d --build
```

### 5. Initialize Database
Once the containers are running:
```bash
# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

### 6. Import Existing Data (Optional)
If you have an exported `.sql` file (from `export_db.sh`):
```bash
# Copy file to container
docker cp your_backup.sql rhms_db:/backup.sql

# Import
docker-compose exec db sh -c 'mysql -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE < /backup.sql'
```

---

## Option 2: Manual Deployment (Nginx + Gunicorn)

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv python3-dev libmysqlclient-dev nginx mysql-server
```

### 2. Setup Database
```bash
sudo mysql -u root -p
```
```sql
CREATE DATABASE revana_hms_db CHARACTER SET utf8mb4;
CREATE USER 'rhms_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON revana_hms_db.* TO 'rhms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Setup Application
```bash
git clone <YOUR_REPOSITORY_URL>
cd revana_hms

# Create Virtual Env
python3 -m venv venv
source venv/bin/activate

# Install Deps
pip install -r requirements.txt
pip install gunicorn

# Setup .env
nano .env  # Add DB credentials (DB_HOST=localhost)

# Prepare App
python manage.py migrate
python manage.py collectstatic
```

### 4. Configure Gunicorn & Nginx
(Refer to standard Django deployment guides for creating systemd services and Nginx blocks).

## Database Backup/Export

To export your database from the current system, use the provided script:
```bash
./export_db.sh
```
This will create a `db_backup_YYYYMMDD_HHMMSS.sql` file in the current directory.
