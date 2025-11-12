# Collections API

## Overview

The Collections API allows you to programmatically manage PocketBase collections, including creating, updating, deleting, and configuring collections.

## List Collections

```http
GET /api/collections
Authorization: Bearer {admin_token}
```

Response:
```json
{
  "page": 1,
  "perPage": 50,
  "totalItems": 3,
  "totalPages": 1,
  "items": [
    {
      "id": "collection_id",
      "name": "posts",
      "type": "base",
      "system": false,
      "schema": [...],
      "options": {...},
      "listRule": null,
      "viewRule": null,
      "createRule": null,
      "updateRule": null,
      "deleteRule": null,
      "created": "2024-01-01T00:00:00.000Z",
      "updated": "2024-01-01T00:00:00.000Z"
    }
  ]
}
```

## Get Single Collection

```http
GET /api/collections/{collectionId}
Authorization: Bearer {admin_token}
```

## Create Collection

```http
POST /api/collections
Content-Type: application/json
Authorization: Bearer {admin_token}

{
  "name": "products",
  "type": "base",
  "schema": [
    {
      "name": "title",
      "type": "text",
      "required": true,
      "options": {
        "min": 1,
        "max": 200
      }
    },
    {
      "name": "price",
      "type": "number",
      "required": true,
      "options": {
        "min": 0
      }
    }
  ],
  "listRule": "status = 'published'",
  "viewRule": "status = 'published'",
  "createRule": "@request.auth.id != ''",
  "updateRule": "@request.auth.role = 'admin'",
  "deleteRule": "@request.auth.role = 'admin'"
}
```

## Update Collection

```http
PATCH /api/collections/{collectionId}
Content-Type: application/json
Authorization: Bearer {admin_token}

{
  "name": "products",
  "schema": [
    // updated schema
  ],
  "options": {
    "allowEmailAuth": true,
    "allowOAuth2Auth": false,
    "allowUsernameAuth": false,
    "exceptEmailDomains": [],
    "manageAccounts": false,
    "minPasswordLength": 8,
    "onlyEmailDomains": [],
    "requireEmail": true
  }
}
```

## Delete Collection

```http
DELETE /api/collections/{collectionId}
Authorization: Bearer {admin_token}
```

## Import Collections

```http
POST /api/collections/import
Content-Type: application/json
Authorization: Bearer {admin_token}

{
  "collections": [
    {
      "name": "posts",
      "type": "base",
      "schema": [...],
      "options": {...},
      "listRule": "...",
      "viewRule": "...",
      "createRule": "...",
      "updateRule": "...",
      "deleteRule": "..."
    }
  ]
}
```

## Export Collections

```http
GET /api/collections/export?collections=posts,comments
Authorization: Bearer {admin_token}
```

---

**Note:** This is a placeholder file. See [core/collections.md](../core/collections.md) for comprehensive collection documentation.
