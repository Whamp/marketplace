# Go Overview - PocketBase

## Overview

PocketBase can be extended using Go, allowing you to:
- Add custom API endpoints
- Implement event hooks
- Create custom database migrations
- Build scheduled jobs
- Add custom middleware
- Integrate external services
- Extend authentication

## Project Structure

```
myapp/
├── go.mod
├── pocketbase.go
├── migrations/
│   └── 1703123456_initial.go
├── hooks/
│   └── hooks.go
└── main.go
```

## Creating a Go Extension

### 1. Initialize Go Module

```bash
go mod init myapp
```

### 2. Install PocketBase SDK

```bash
go get github.com/pocketbase/pocketbase@latest
```

### 3. Basic PocketBase App

Create `main.go`:

```go
package main

import (
    "log"
    "net/http"

    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/core"
)

func main() {
    app := pocketbase.New()

    // Add custom API endpoint
    app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
        // Custom routes
        e.Router.GET("/api/hello", func(e *core.RequestEvent) error {
            return e.JSON(200, map[string]string{
                "message": "Hello from Go!",
            })
        })

        return nil
    })

    // Start the app
    if err := app.Start(); err != nil {
        log.Fatal(err)
    }
}
```

### 4. Run the Application

```bash
go run main.go pocketbase.go serve --http=0.0.0.0:8090
```

## Core Concepts

### Event Hooks

Execute code on specific events:

```go
// On record create
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    log.Println("Post created:", e.Record.GetString("title"))
    return nil
})

// On record update
app.OnRecordUpdate("posts").Add(func(e *core.RecordUpdateEvent) error {
    log.Println("Post updated:", e.Record.GetString("title"))
    return nil
})

// On record delete
app.OnRecordDelete("posts").Add(func(e *core.RecordDeleteEvent) error {
    log.Println("Post deleted:", e.Record.GetString("title"))
    return nil
})

// On authentication
app.OnRecordAuth().Add(func(e *core.RecordAuthEvent) error {
    log.Println("User authenticated:", e.Record.GetString("email"))
    return nil
})
```

### Event Arguments

**RecordCreateEvent:**
```go
type RecordCreateEvent struct {
    Record         *Record // New record
    Collection     *Collection
    HttpContext    *gin.Context
}
```

**RecordUpdateEvent:**
```go
type RecordUpdateEvent struct {
    Record         *Record // Updated record
    RecordOriginal *Record // Original record before update
    Collection     *Collection
    HttpContext    *gin.Context
}
```

**RecordDeleteEvent:**
```go
type RecordDeleteEvent struct {
    Record         *Record // Record being deleted
    Collection     *Collection
}
```

**RecordAuthEvent:**
```go
type RecordAuthEvent struct {
    Record         *Record // Authenticated user
    IsCreate       bool    // True if user just registered
    HttpContext    *gin.Context
}
```

## Custom API Endpoints

### Create GET Endpoint

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    e.Router.GET("/api/stats", func(e *core.RequestEvent) error {
        // Get current user (if authenticated)
        user, _ := e.App.Auth().GetUserFromRequest(e.HttpContext)

        // Query database
        totalPosts, _ := e.App.Dao().FindRecordsByExpr("posts")
        totalUsers, _ := e.App.Dao().FindRecordsByExpr("users")

        return e.JSON(200, map[string]interface{}{
            "total_posts": len(totalPosts),
            "total_users": len(totalUsers),
            "authenticated": user != nil,
        })
    })

    return nil
})
```

### Create POST Endpoint

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    e.Router.POST("/api/search", func(e *core.RequestEvent) error {
        // Parse request body
        var req struct {
            Query string `json:"query"`
        }
        if err := e.BindBody(&req); err != nil {
            return e.BadRequest(err.Error())
        }

        // Search posts
        records, err := e.App.Dao().FindRecordsByExpr("posts", dao.Where(
            "title LIKE ?", "%"+req.Query+"%",
        ))
        if err != nil {
            return e.InternalServerError("Search failed", err)
        }

        return e.JSON(200, map[string]interface{}{
            "results": records,
            "count":   len(records),
        })
    })

    return nil
})
```

### Custom Middleware

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    e.Router.Use(func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            // Add CORS headers
            w.Header().Set("Access-Control-Allow-Origin", "*")
            w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
            w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

            if r.Method == "OPTIONS" {
                w.WriteHeader(http.StatusOK)
                return
            }

            next.ServeHTTP(w, r)
        })
    })

    return nil
})
```

## Database Operations

### Find Records

```go
// Find single record
record, err := app.Dao().FindRecordById("posts", "RECORD_ID")

// Find multiple records
records, err := app.Dao().FindRecordsByExpr("posts", dao.Where(
    "status = ?", "published",
))

// Find with pagination
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Where("status = ?", "published"),
    dao.Offset(0),
    dao.Limit(50),
)

// Find with relations
record, err := app.Dao().FindRecordById("posts", "id")
app.Dao().ExpandRecord(record, []string{"author", "comments"}, nil)
```

### Create Records

```go
// Create record
record := dao.NewRecord("posts")
record.Set("title", "My Post")
record.Set("content", "Post content")
record.Set("author", "USER_ID")

if err := app.Dao().SaveRecord(record); err != nil {
    return err
}
```

### Update Records

```go
// Find and update
record, err := app.Dao().FindRecordById("posts", "id")
if err != nil {
    return err
}

record.Set("title", "Updated Title")
record.Set("content", "Updated content")

if err := app.Dao().SaveRecord(record); err != nil {
    return err
}
```

### Delete Records

```go
record, err := app.Dao().FindRecordById("posts", "id")
if err != nil {
    return err
}

if err := app.Dao().DeleteRecord(record); err != nil {
    return err
}
```

### Query Builder

```go
// Complex queries
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Where("status = ?", "published"),
    dao.Where("created >= ?", "2024-01-01"),
    dao.OrderBy("created DESC"),
    dao.Offset(0),
    dao.Limit(50),
)

// Or operator
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Or(
        dao.Where("status = ?", "published"),
        dao.Where("author = ?", userId),
    ),
)
```

## Event Hooks Examples

### Auto-populate Fields

```go
// Auto-set author on post create
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    // Set author to current user
    user, _ := e.App.Auth().GetUserFromRequest(e.HttpContext)
    if user != nil {
        e.Record.Set("author", user.Id)
    }
    return nil
})

// Auto-set slug from title
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    title := e.Record.GetString("title")
    slug := strings.ToLower(strings.ReplaceAll(title, " ", "-"))
    e.Record.Set("slug", slug)
    return nil
})
```

### Validation

```go
// Custom validation
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    title := e.Record.GetString("title")
    if len(title) < 5 {
        return errors.New("title must be at least 5 characters")
    }
    return nil
})

// Check permissions
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    user, _ := e.App.Auth().GetUserFromRequest(e.HttpContext)
    if user == nil {
        return errors.New("authentication required")
    }

    // Check user role
    if user.GetString("role") != "admin" && user.GetString("role") != "author" {
        return errors.New("insufficient permissions")
    }

    return nil
})
```

### Cascading Updates

```go
// When post is updated, update related comments
app.OnRecordUpdate("posts").Add(func(e *core.RecordUpdateEvent) error {
    // Check if status changed
    oldStatus := e.RecordOriginal.GetString("status")
    newStatus := e.Record.GetString("status")

    if oldStatus != newStatus && newStatus == "published" {
        // Notify subscribers or update related data
        comments, _ := e.App.Dao().FindRecordsByExpr("comments",
            dao.Where("post = ?", e.Record.Id),
        )

        for _, comment := range comments {
            comment.Set("status", "approved")
            e.App.Dao().SaveRecord(comment)
        }
    }

    return nil
})
```

### Send Notifications

```go
// Send email when post is published
app.OnRecordUpdate("posts").Add(func(e *core.RecordUpdateEvent) error {
    oldStatus := e.RecordOriginal.GetString("status")
    newStatus := e.Record.GetString("status")

    if oldStatus != "published" && newStatus == "published" {
        // Get author email
        author, _ := e.App.Dao().FindRecordById("users", e.Record.GetString("author"))
        if author != nil {
            // Send email (implement your email sending logic)
            log.Println("Sending notification to:", author.GetString("email"))
        }
    }

    return nil
})
```

### Log Activities

```go
// Log all record changes
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    return logActivity(e.App, "create", "posts", e.Record.Id, e.HttpContext)
})

app.OnRecordUpdate("posts").Add(func(e *core.RecordUpdateEvent) error {
    return logActivity(e.App, "update", "posts", e.Record.Id, e.HttpContext)
})

app.OnRecordDelete("posts").Add(func(e *core.RecordDeleteEvent) error {
    return logActivity(e.App, "delete", "posts", e.Record.Id, e.HttpContext)
})

func logActivity(app core.App, action, collection, recordId string, c *gin.Context) error {
    activity := dao.NewRecord("activity")
    activity.Set("action", action)
    activity.Set("collection", collection)
    activity.Set("record_id", recordId)

    // Get user info
    user, _ := app.Auth().GetUserFromRequest(c)
    if user != nil {
        activity.Set("user", user.Id)
    }

    // Get IP
    activity.Set("ip", c.ClientIP())

    return app.Dao().SaveRecord(activity)
}
```

## Scheduled Jobs

### Create Background Job

```go
// Register job
app.Root().Cron().Add("0 2 * * *", "daily-backup", func() error {
    log.Println("Running daily backup...")

    // Export data
    backupDir := "./backups"
    if err := os.MkdirAll(backupDir, 0755); err != nil {
        return err
    }

    // Your backup logic here
    log.Println("Backup completed")

    return nil
})

// Or use one-off job
app.OnServe().Add(func(e *core.ServeEvent) error {
    e.App.Root().Cron().Add("@every 5m", "cleanup", func() error {
        log.Println("Running cleanup task...")

        // Cleanup logic
        return nil
    })

    return nil
})
```

## File Handling

### Custom File Upload

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    e.Router.POST("/api/upload", func(e *core.RequestEvent) error {
        // Get file from request
        fileHeader, err := e.HttpContext.FormFile("file")
        if err != nil {
            return e.BadRequest("No file uploaded", err)
        }

        // Open file
        file, err := fileHeader.Open()
        if err != nil {
            return e.InternalServerError("Failed to open file", err)
        }
        defer file.Close()

        // Create record with file
        record := dao.NewRecord("uploads")
        record.Set("name", fileHeader.Filename)
        record.Set("size", fileHeader.Size)
        record.Set("type", fileHeader.Header.Get("Content-Type"))

        // Save file
        files := formfile.NewFiles(fileHeader)
        if err := e.App.Dao().SaveRecord(record, files...); err != nil {
            return e.InternalServerError("Failed to save file", err)
        }

        return e.JSON(200, record)
    })

    return nil
})
```

## Custom Auth Provider

```go
// Custom OAuth provider
app.OnRecordAuthWithOAuth2().Add(func(e *core.RecordAuthWithOAuth2Event) error {
    if e.Provider != "custom" {
        return nil
    }

    // Fetch user info from custom provider
    userInfo, err := fetchCustomUserInfo(e.OAuth2UserData)
    if err != nil {
        return err
    }

    // Find or create user
    user, err := e.App.Dao().FindAuthRecordByData("users", "email", userInfo.Email)
    if err != nil {
        // Create new user
        user = dao.NewRecord("users")
        user.Set("email", userInfo.Email)
        user.Set("password", "") // OAuth users don't need password
        user.Set("emailVisibility", false)
        user.Set("verified", true)
        user.Set("name", userInfo.Name)
        e.App.Dao().SaveRecord(user)
    }

    e.Record = user
    return nil
})
```

## Testing

### Unit Tests

```go
package main

import (
    "testing"

    "github.com/pocketbase/pocketbase"
    "github.com/pocketbase/pocketbase/core"
    "github.com/pocketbase/pocketbase/tests"
)

func TestCustomEndpoint(t *testing.T) {
    app := pocketbase.NewWithConfig(config{})

    // Add test endpoint
    app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
        e.Router.GET("/api/test", func(e *core.RequestEvent) error {
            return e.JSON(200, map[string]string{
                "status": "ok",
            })
        })
        return nil
    })

    e := tests.NewRequestEvent(app, nil)
    // Test endpoint
    e.GET("/api/test").Expect(t).Status(200).JSON().Equal(map[string]interface{}{
        "status": "ok",
    })
}
```

### Integration Tests

```go
func TestRecordCreation(t *testing.T) {
    app := pocketbase.New()
    app.MustSeed()

    client := tests.NewClient(app)

    // Test authenticated request
    auth := client.AuthRecord("users", "test@example.com", "password")
    post := client.CreateRecord("posts", map[string]interface{}{
        "title":   "Test Post",
        "content": "Test content",
    }, auth.Token)

    if post.GetString("title") != "Test Post" {
        t.Errorf("Expected title 'Test Post', got %s", post.GetString("title"))
    }
}
```

## Deployment

### Build and Run

```bash
# Build
go build -o myapp main.go

# Run
./myapp serve --http=0.0.0.0:8090
```

### Docker Deployment

```dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o myapp main.go

FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/

COPY --from=builder /app/myapp .
COPY --from=builder /app/pocketbase ./

CMD ["./myapp", "serve", "--http=0.0.0.0:8090"]
```

## Best Practices

### 1. Error Handling

```go
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    if err := validatePost(e.Record); err != nil {
        return err
    }
    return nil
})

func validatePost(record *dao.Record) error {
    title := record.GetString("title")
    if len(title) == 0 {
        return errors.New("title is required")
    }
    if len(title) > 200 {
        return errors.New("title too long")
    }
    return nil
}
```

### 2. Logging

```go
import "github.com/pocketbase/pocketbase/logs"

app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    logs.Info("Post created", "id", e.Record.Id, "title", e.Record.GetString("title"))
    return nil
})
```

### 3. Security

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    // Rate limiting middleware
    limiter := rate.NewLimiter(10, 20) // 10 req/sec, burst 20

    e.Router.Use(func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            if !limiter.Allow() {
                http.Error(w, "Rate limit exceeded", 429)
                return
            }
            next.ServeHTTP(w, r)
        })
    })

    return nil
})
```

### 4. Configuration

```go
type Config struct {
    ExternalAPIKey string
    EmailFrom      string
}

func (c Config) Name() string {
    return "myapp"
}

func main() {
    app := pocketbase.NewWithConfig(Config{
        ExternalAPIKey: os.Getenv("API_KEY"),
        EmailFrom:      "noreply@example.com",
    })

    // Use config in hooks
    app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
        cfg := e.App.Config().(*Config)
        // Use cfg.ExternalAPIKey
        return nil
    })
}
```

## Common Patterns

### 1. Soft Delete

```go
app.OnRecordDelete("posts").Add(func(e *core.RecordDeleteEvent) error {
    // Instead of deleting, mark as deleted
    e.Record.Set("status", "deleted")
    e.Record.Set("deleted_at", time.Now())
    return e.App.Dao().SaveRecord(e.Record)
})
```

### 2. Audit Trail

```go
app.OnRecordCreate("").Add(func(e *core.RecordCreateEvent) error {
    if e.Collection.Name == "posts" || e.Collection.Name == "comments" {
        e.Record.Set("created_by", e.App.Auth().GetUserFromRequest(e.HttpContext).Id)
        e.Record.Set("created_ip", e.HttpContext.ClientIP())
    }
    return nil
})

app.OnRecordUpdate("").Add(func(e *core.RecordUpdateEvent) error {
    if e.Collection.Name == "posts" || e.Collection.Name == "comments" {
        e.Record.Set("updated_by", e.App.Auth().GetUserFromRequest(e.HttpContext).Id)
        e.Record.Set("updated_at", time.Now())
    }
    return nil
})
```

### 3. Data Synchronization

```go
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    // Sync with external service
    if err := syncToExternalAPI(e.Record); err != nil {
        logs.Warn("Sync failed", "error", err)
    }
    return nil
})

func syncToExternalAPI(record *dao.Record) error {
    // Implement external API sync
    return nil
}
```

## Related Topics

- [Event Hooks](go_event_hooks.md) - Detailed hook documentation
- [Database](go_database.md) - Database operations
- [Routing](go_routing.md) - Custom API endpoints
- [Migrations](go_migrations.md) - Database migrations
- [Testing](go_testing.md) - Testing strategies
- [Logging](go_logging.md) - Logging and monitoring
