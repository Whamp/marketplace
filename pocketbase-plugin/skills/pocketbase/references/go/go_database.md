# Database Operations - Go Extensions

## Overview

PocketBase provides a powerful database API for Go extensions, allowing you to perform complex queries, transactions, and data operations.

## Basic Queries

### Find Records

```go
// Find single record
record, err := app.Dao().FindRecordById("posts", "RECORD_ID")

// Find multiple records with filter
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Where("status = ?", "published"),
    dao.OrderBy("created DESC"),
)

// Find with pagination
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Where("status = ?", "published"),
    dao.Offset(0),
    dao.Limit(50),
)
```

### Query Builder

```go
// Complex queries
records, err := app.Dao().FindRecordsByExpr("posts",
    dao.Where("status = ?", "published"),
    dao.Where("created >= ?", "2024-01-01"),
    dao.Or(
        dao.Where("author = ?", userId),
        dao.Where("featured = ?", true),
    ),
    dao.OrderBy("created DESC"),
    dao.Offset(0),
    dao.Limit(50),
)
```

### Transactions

```go
err := app.Dao().RunInTransaction(func(tx dao.Dao) error {
    // Create post
    post := dao.NewRecord("posts")
    post.Set("title", "New Post")
    if err := tx.SaveRecord(post); err != nil {
        return err
    }

    // Create comment
    comment := dao.NewRecord("comments")
    comment.Set("post", post.Id)
    comment.Set("content", "First comment")
    return tx.SaveRecord(comment)
})
```

---

**Note:** This is a placeholder file. See [go_overview.md](go_overview.md) for comprehensive database documentation.
