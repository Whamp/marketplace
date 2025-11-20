# Claude Code Marketplace of Plugins

This is marketplace of claude code plugins.

https://code.claude.com/docs/en/plugins

https://code.claude.com/docs/en/plugins#add-marketplaces

## Available Plugins:

### 🔧 Browser Tools Plugin `browser-tools-plugin`
**Version:** 1.0.0
**Description:** Efficient browser automation tools using Node.js and Chrome DevTools Protocol for navigation, scripting, and screenshots without MCP overhead

**Key Features:**
- Lightweight Node.js scripts (~300 tokens vs MCP's 13-18k tokens)
- Chrome DevTools Protocol integration
- Screenshot capabilities (full-page or element-specific)
- JavaScript execution in browser context
- Cookie management and import/export
- Element selection and interaction
- Cross-platform support (macOS, Linux, Windows)

**Use Cases:** Web scraping, automated testing, screenshot generation, browser automation

**Keywords:** `browser`, `automation`, `chrome`, `devtools`, `screenshot`, `javascript`

---

### 🗄️ PocketBase Plugin `pocketbase-plugin`
**Version:** 0.0.2
**Description:** Comprehensive PocketBase development and deployment toolkit with 40+ reference files covering setup, API integration, Go extensions, security rules, schema templates, and deployment guides

**Key Features:**
- Complete PocketBase knowledge base (40+ reference files)
- API documentation covering all 9 API endpoints
- Go extensions documentation (17 files)
- Security rules and best practices
- Schema templates for common applications
- Production deployment guides
- Specialized research agent for PocketBase

**Use Cases:** Backend-as-a-service development, REST API creation, real-time applications, authentication systems

**Keywords:** `pocketbase`, `backend-as-a-service`, `database`, `rest-api`, `realtime`, `authentication`

---

### 🧠 Gemini CLI Integration Plugin `gemini-cli-plugin`
**Version:** 0.1.0
**Description:** Integration with Google Gemini CLI for large codebase analysis using massive context windows

**Key Features:**
- Large codebase analysis with @ syntax for file inclusion
- Implementation verification workflows
- Security and quality assurance capabilities
- Session management and resumption
- Advanced CLI options with approval modes
- Extensions and MCP integration support

**Use Cases:** Analyzing entire codebases, multi-file comparison, architecture understanding, pattern detection, automated workflows

**Keywords:** `gemini`, `cli`, `codebase-analysis`, `context-window`, `google-ai`

---

### 📧 MailHog Plugin `mailhog-plugin`
**Version:** 1.0.0
**Description:** Email testing server setup and management for development and testing environments

**Key Features:**
- Complete MailHog server management
- SMTP server configuration (default port 1025)
- HTTP API/UI for email viewing (default port 8025)
- Multiple storage options (memory, MongoDB, Maildir)
- Network simulation with Jim for chaotic testing
- Authentication and security configuration
- Development integration patterns

**Use Cases:** Development email testing, automated email verification, bulk email testing, production email capture

**Keywords:** `mailhog`, `email`, `testing`, `smtp`, `development`, `debugging`

---

## Plugin Status

- ✅ **Fully Available:** 4 plugins (browser-tools, pocketbase, gemini-cli-integration, mailhog)
- 🚧 **In Progress:** apex2-plugin

## Marketplace Information

- **Marketplace Name:** whamp-claude-tools
- **Owner:** Will Hampson
- **Repository:** https://github.com/Whamp/marketplace
- **License:** MIT