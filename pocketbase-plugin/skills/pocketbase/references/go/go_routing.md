# Routing - Go Extensions

## Overview

Create custom API endpoints and middleware using PocketBase's routing system.

## Custom Endpoints

```go
app.OnBeforeServe().Add(func(e *core.ServeEvent) error {
    // GET endpoint
    e.Router.GET("/api/custom", func(e *core.RequestEvent) error {
        return e.JSON(200, map[string]string{"status": "ok"})
    })

    // POST endpoint
    e.Router.POST("/api/custom", func(e *core.RequestEvent) error {
        return e.JSON(200, map[string]string{"message": "created"})
    })

    return nil
})
```

---

**Note:** See [go_overview.md](go_overview.md) for detailed routing documentation.
