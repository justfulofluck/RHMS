# 🚀 Quick Deployment Checklist for aaPanel

## Before You Start
- [ ] Have Docker Hub account ready
- [ ] Have aaPanel server access
- [ ] Know your server IP address

## Step 1: Build & Push (Local Machine)
```bash
cd /home/bhavan/Desktop/RHMS/revana_hms

# Run the automated script
./build-and-push.sh YOUR_DOCKERHUB_USERNAME

# Example: ./build-and-push.sh johndoe
```

## Step 2: Update Configuration Files

### Edit `docker-compose.aapanel.yml`
Replace line 23:
```yaml
image: YOUR_DOCKERHUB_USERNAME/rhms:latest
```
With your actual username:
```yaml
image: johndoe/rhms:latest
```

### Create `.env` file
Copy `.env.aapanel.template` to `.env` and update:
- [ ] DB_PASSWORD (use strong password)
- [ ] DB_ROOT_PASSWORD (use strong password)
- [ ] SECRET_KEY (generate random string)
- [ ] ALLOWED_HOSTS (add your domain/IP)
- [ ] Email settings

## Step 3: Upload to aaPanel Server

Upload these 3 files to your server:
1. `docker-compose.aapanel.yml`
2. `.env`
3. `nginx.conf`

## Step 4: Deploy in aaPanel

1. **Login to aaPanel** → Docker → Compose
2. **Add Project**
   - Name: `rhms`
   - Upload: `docker-compose.aapanel.yml`
3. **Configure Environment**
   - Upload `.env` file to project directory
4. **Start Services**
   - Click "Start" button
   - Wait for containers to be healthy (green status)

## Step 5: Initial Setup

In aaPanel Docker Manager:
1. Click on `rhms_web` container
2. Open **Terminal**
3. Run:
```bash
python manage.py createsuperuser
```

## Step 6: Access Application

- **Homepage**: `http://YOUR_SERVER_IP`
- **Admin**: `http://YOUR_SERVER_IP/admin`
- **Book Appointment**: `http://YOUR_SERVER_IP/book-appointment/`

## Troubleshooting

### Container won't start?
- Check logs in aaPanel Docker Manager
- Verify `.env` file is in correct location
- Ensure all passwords are set

### Can't access website?
- Check firewall: Port 80 must be open
- Verify container status is "Running"
- Check nginx logs

### Database errors?
- Wait for MySQL to be healthy (takes ~30 seconds)
- Check DB credentials in `.env`

## Updating Application

```bash
# 1. Rebuild and push new image
./build-and-push.sh YOUR_DOCKERHUB_USERNAME

# 2. In aaPanel, restart the project
# Docker → Compose → Select rhms → Restart
```

## Backup

In aaPanel:
- **Database**: Docker → Volumes → mysql_data → Backup
- **Media Files**: Docker → Volumes → media_volume → Backup

---

**Need Help?** Check `AAPANEL_DEPLOYMENT.md` for detailed instructions.
