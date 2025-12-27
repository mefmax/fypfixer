#!/bin/bash
# FYPGlow Database Backup Script

BACKUP_DIR="/var/backups/fypglow"
RETENTION_DAYS=7
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cd /opt/fypglow
docker compose exec -T db pg_dump -U fypglow fypglow > "$BACKUP_DIR/fypglow_$DATE.sql"

# Compress
gzip "$BACKUP_DIR/fypglow_$DATE.sql"

# Remove old backups (older than 7 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +$RETENTION_DAYS -delete

# Log
echo "$(date): Backup completed - fypglow_$DATE.sql.gz" >> /var/log/fypglow-backup.log
