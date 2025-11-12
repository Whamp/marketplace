# Event Hooks - Go Extensions

## Overview

Event hooks allow you to execute custom logic when specific events occur in PocketBase, such as record creation, updates, authentication, or API requests.

## Hook Types

### Record Hooks
- `OnRecordCreate()` - Before/after record creation
- `OnRecordUpdate()` - Before/after record updates
- `OnRecordDelete()` - Before/after record deletion
- `OnRecordList()` - Before/after listing records
- `OnRecordView()` - Before/after viewing a record

### Auth Hooks
- `OnRecordAuth()` - After authentication
- `OnRecordAuthWithPassword()` - Password authentication
- `OnRecordAuthWithOAuth2()` - OAuth2 authentication
- `OnRecordRequestPasswordReset()` - Password reset request
- `OnRecordConfirmPasswordReset()` - Password reset confirmation

### Serve Hooks
- `OnBeforeServe()` - Before HTTP server starts
- `OnAfterServe()` - After HTTP server starts

## Examples

### Auto-populate Fields

```go
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    // Set author to current user
    user, _ := e.App.Auth().GetUserFromRequest(e.HttpContext)
    if user != nil {
        e.Record.Set("author", user.Id)
    }

    // Auto-generate slug from title
    title := e.Record.GetString("title")
    slug := strings.ToLower(strings.ReplaceAll(title, " ", "-"))
    e.Record.Set("slug", slug)

    return nil
})
```

### Validation

```go
app.OnRecordCreate("posts").Add(func(e *core.RecordCreateEvent) error {
    title := e.Record.GetString("title")
    if len(title) < 5 {
        return errors.New("title must be at least 5 characters")
    }

    // Check for duplicate titles
    existing, err := e.App.Dao().FindRecordsByExpr("posts",
        dao.Where("title = ?", title),
    )
    if err == nil && len(existing) > 0 {
        return errors.New("title already exists")
    }

    return nil
})
```

### Cascading Updates

```go
app.OnRecordUpdate("posts").Add(func(e *core.RecordUpdateEvent) error {
    // When post is published, update related comments
    oldStatus := e.RecordOriginal.GetString("status")
    newStatus := e.Record.GetString("status")

    if oldStatus != "published" && newStatus == "published" {
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

---

**Note:** This is a placeholder file. See [go_overview.md](go_overview.md) for detailed hook documentation.
