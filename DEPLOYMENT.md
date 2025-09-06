# Deployment Guide

This guide covers different deployment strategies for the FastAPI Vue Starter application.

## Table of Contents

- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Production Deployment](#production-deployment)
- [Environment Variables](#environment-variables)
- [Database Setup](#database-setup)
- [SSL/HTTPS Setup](#sslhttps-setup)

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (optional, SQLite used by default)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Initialize database
alembic upgrade head

# Run the server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
cd frontend
npm install

# Copy environment file
cp .env.example .env

# Run development server
npm run dev
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Docker Deployment

### Development with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Production with Docker Compose

```bash
# Start with production profile
docker-compose --profile production up -d

# This includes Nginx reverse proxy
```

## Production Deployment

### Using Docker on a VPS

1. **Server Setup**
   ```bash
   # Install Docker and Docker Compose
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   sudo usermod -aG docker $USER
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

2. **Clone and Configure**
   ```bash
   git clone <your-repo-url> fastapi-vue-app
   cd fastapi-vue-app
   
   # Configure environment variables
   cp backend/.env.example backend/.env
   cp frontend/.env.example frontend/.env
   
   # Edit configuration for production
   nano backend/.env
   nano frontend/.env
   ```

3. **Deploy**
   ```bash
   # Build and start services
   docker-compose --profile production up -d
   
   # Run database migrations
   docker-compose exec backend alembic upgrade head
   ```

### Using Kubernetes

See `k8s/` directory for Kubernetes deployment files (coming soon).

## Environment Variables

### Backend (.env)

```env
# Required
SECRET_KEY=your-super-secret-key-change-in-production
DATABASE_URL=postgresql://user:password@localhost/dbname

# OAuth (Optional)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret

# Email (Optional)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_FROM=your-email@gmail.com

# CORS
FRONTEND_URL=https://yourdomain.com
BACKEND_CORS_ORIGINS=["https://yourdomain.com"]
```

### Frontend (.env)

```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_APP_TITLE=Your App Name
```

## Database Setup

### PostgreSQL Setup

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # Start service
   sudo systemctl start postgresql
   sudo systemctl enable postgresql
   ```

2. **Create Database and User**
   ```bash
   sudo -u postgres psql
   
   CREATE DATABASE fastapi_vue_starter;
   CREATE USER appuser WITH ENCRYPTED PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE fastapi_vue_starter TO appuser;
   \q
   ```

3. **Update Connection String**
   ```env
   DATABASE_URL=postgresql://appuser:your_password@localhost/fastapi_vue_starter
   ```

### Database Migrations

```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## SSL/HTTPS Setup

### Using Certbot with Nginx

1. **Install Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   ```

2. **Update Nginx Configuration**
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       
       # Redirect HTTP to HTTPS
       return 301 https://$server_name$request_uri;
   }
   
   server {
       listen 443 ssl http2;
       server_name yourdomain.com;
       
       # SSL certificates will be added by Certbot
       
       # Your existing configuration...
   }
   ```

3. **Generate Certificates**
   ```bash
   sudo certbot --nginx -d yourdomain.com
   ```

4. **Auto-renewal**
   ```bash
   # Test renewal
   sudo certbot renew --dry-run
   
   # Add to crontab
   echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -
   ```

## Health Checks and Monitoring

### Application Health Checks

- Backend: `GET /health`
- Frontend: `GET /health`

### Monitoring Setup

Consider setting up:
- **Prometheus** + **Grafana** for metrics
- **Loki** for log aggregation
- **Uptime monitoring** (e.g., UptimeRobot)

### Backup Strategy

1. **Database Backups**
   ```bash
   # Create backup script
   #!/bin/bash
   pg_dump -h localhost -U appuser -d fastapi_vue_starter | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
   ```

2. **Automated Backups**
   ```bash
   # Add to crontab for daily backups
   0 2 * * * /path/to/backup_script.sh
   ```

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check `BACKEND_CORS_ORIGINS` setting
   - Ensure frontend URL is correctly configured

2. **Database Connection**
   - Verify PostgreSQL is running
   - Check connection string format
   - Ensure user has correct permissions

3. **OAuth Issues**
   - Verify redirect URIs in OAuth provider settings
   - Check client ID and secret configuration
   - Ensure HTTPS for production OAuth

4. **Email Not Working**
   - Check SMTP settings
   - Verify app password for Gmail
   - Test email configuration

### Logs

```bash
# Docker logs
docker-compose logs backend
docker-compose logs frontend
docker-compose logs nginx

# Application logs
tail -f /var/log/app/backend.log
tail -f /var/log/nginx/access.log
```

## Security Checklist

- [ ] Change default secret key
- [ ] Use HTTPS in production
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting
- [ ] Enable SQL injection protection
- [ ] Configure proper firewall rules
- [ ] Regular security updates
- [ ] Monitor for vulnerabilities
- [ ] Backup strategy in place
- [ ] Environment variables secured

## Performance Optimization

1. **Frontend**
   - Enable gzip compression
   - Use CDN for static assets
   - Implement caching headers
   - Optimize images

2. **Backend**
   - Use connection pooling
   - Implement Redis caching
   - Optimize database queries
   - Use async operations

3. **Database**
   - Create appropriate indexes
   - Regular VACUUM and ANALYZE
   - Monitor query performance
   - Consider read replicas for high traffic