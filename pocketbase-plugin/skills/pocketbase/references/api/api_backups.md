# Backups API

## Overview

The Backups API manages database backups, exports, and imports.

## List Backups

```http
GET /api/backups
Authorization: Bearer {admin_token}
```

## Create Backup

```http
POST /api/backups
Content-Type: application/json
Authorization: Bearer {admin_token}

{
  "name": "backup-2024-01-01"
}
```

## Download Backup

```http
GET /api/backups/{backupId}/download
Authorization: Bearer {admin_token}
```

## Upload Backup

```http
POST /api/backups/upload
Content-Type: multipart/form-data
Authorization: Bearer {admin_token}

file: backup.sql
```

## Restore Backup

```http
POST /api/backups/{backupId}/restore
Authorization: Bearer {admin_token}
```

---

**Note:** This is a placeholder file. See [core/going_to_production.md](../core/going_to_production.md#backup-strategy) for backup strategies.
