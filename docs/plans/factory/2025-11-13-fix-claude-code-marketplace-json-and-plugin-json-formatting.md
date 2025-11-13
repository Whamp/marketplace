Summary of issues found:
- Top-level .claude-plugin/marketplace.json is not using the official schema (missing required `plugins[]`, includes unsupported fields like `id`, `manifestUrl`, `verified`, `addedAt`, `tags`).
- pocketbase-plugin/.claude-plugin/plugin.json already matches the manifest schema (no unsupported keys), so no content changes needed there.

What I will change:
1) Replace .claude-plugin/marketplace.json with a schema-compliant file, naming the marketplace `whamp-claude-tools` and listing the PocketBase plugin via a relative source path.
2) Keep pocketbase-plugin/.claude-plugin/plugin.json as-is (it already conforms). If you want, I can add optional metadata fields, but not required.

Proposed new files (exact content):

.marketplace at repo root: .claude-plugin/marketplace.json
```json
{
  "name": "whamp-claude-tools",
  "owner": { "name": "Will Hampson" },
  "metadata": {
    "description": "Claude Code plugins and skills by Whamp"
  },
  "plugins": [
    {
      "name": "pocketbase",
      "source": "./pocketbase-plugin",
      "description": "Comprehensive PocketBase development and deployment toolkit with 40+ reference files covering setup, API integration, Go extensions, security rules, schema templates, and deployment guides",
      "version": "0.0.1",
      "author": { "name": "Will Hampson" },
      "homepage": "https://github.com/Whamp/pocketbase-plugin",
      "repository": "https://github.com/Whamp/marketplace/tree/main/pocketbase-plugin",
      "keywords": [
        "pocketbase",
        "backend-as-a-service",
        "database",
        "rest-api",
        "realtime",
        "authentication"
      ]
    }
  ]
}
```

PocketBase plugin manifest (no change needed, for reference): pocketbase-plugin/.claude-plugin/plugin.json
```json
{
  "name": "pocketbase",
  "description": "Comprehensive PocketBase development and deployment toolkit with 40+ reference files covering setup, API integration, Go extensions, security rules, schema templates, and deployment guides",
  "version": "0.0.1",
  "author": { "name": "Will Hampson" },
  "keywords": [
    "pocketbase",
    "backend-as-a-service",
    "database",
    "rest-api",
    "realtime",
    "authentication"
  ],
  "repository": "https://github.com/Whamp/marketplace/tree/main/pocketbase-plugin",
  "license": "MIT",
  "homepage": "https://github.com/Whamp/pocketbase-plugin"
}
```

Validation and cleanup (after I apply edits):
- Run: `claude plugin validate .` to confirm both files pass schema checks.
- If you still see the prior error from an old install: remove and re-add this local marketplace, then reinstall the plugin:
  - `/plugin marketplace remove whamp-claude-tools` (if present)
  - `/plugin marketplace add ./`  (from repo root)
  - `/plugin install pocketbase@whamp-claude-tools`
- The unrelated payload error comes from a different marketplace; you can remove or fix that marketplace separately.

Shall I proceed to apply these edits and validate?