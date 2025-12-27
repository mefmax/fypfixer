# FYPGlow Deployment Guide

## Server Requirements
- Ubuntu 24.04 LTS
- Docker 29+
- Nginx
- Let's Encrypt SSL

## Security Configuration

### SSH (/etc/ssh/sshd_config)
```
PermitRootLogin yes
PasswordAuthentication yes
MaxAuthTries 5
```

### Nginx Security Headers
```nginx
server_tokens off;
add_header X-Frame-Options "DENY" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

### TLS Configuration
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_prefer_server_ciphers on;
```

### Docker Log Limits (/etc/docker/daemon.json)
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

## Backup
- Script: `/opt/fypglow/backup.sh`
- Schedule: Daily at 3:00 UTC
- Location: `/var/backups/fypglow/`
- Retention: 7 days

## Monitoring
- Telegram alerts via cron health check
- fail2ban: sshd, fypglow-auth, fypglow-ddos jails
- Request logging to database

## Deploy Steps
1. `git pull origin main`
2. `docker compose build --no-cache`
3. `docker compose up -d`
4. `docker compose exec backend flask db upgrade`
5. Verify: `curl localhost:8000/api/health`
