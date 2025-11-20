# MailHog Plugin for Claude Code

A comprehensive MailHog email testing server management toolkit that provides complete SMTP testing, email capture, development integration, and automated email workflow testing capabilities.

## Overview

MailHog is an essential development tool that captures all emails sent from your application during development and testing, preventing accidental delivery to real users while providing full visibility into email functionality. This plugin offers complete MailHog server management with SMTP testing, email capture, development integration, and automated email workflow testing.

## Features

- **🚀 Quick Setup** - One-command MailHog server startup with sensible defaults
- **📧 Email Capture** - Complete SMTP server for capturing all outgoing emails
- **🔧 Configuration Management** - Advanced configuration for storage, authentication, and networking
- **🐳 Docker Integration** - Pre-configured Docker Compose setups
- **⚡ Automated Testing** - Scripts for email workflow automation and testing
- **🌐 Development Integration** - Ready-to-use configurations for popular frameworks
- **📊 Monitoring & Debugging** - Built-in health checks and performance optimization
- **🔒 Security Features** - Authentication and secure configuration options

## Quick Start

### 1. Start MailHog Server

```bash
# Basic setup with memory storage
mailhog

# Access the web interface at http://localhost:8025
# SMTP server runs on port 1025
```

### 2. Configure Your Application

Configure your application to use MailHog as its SMTP server:

**Environment Variables:**
```bash
export SMTP_HOST=localhost
export SMTP_PORT=1025
export SMTP_USER=
export SMTP_PASS=
export SMTP_TLS=false
```

### 3. Send Test Email

```bash
# Use the provided test script
./scripts/send_test_email.sh --to test@example.com --subject "Test Email" --body "Hello MailHog!"
```

### 4. View Captured Emails

Open http://localhost:8025 in your browser to see all captured emails.

## Installation

### Option 1: Install MailHog Binary

```bash
# Download latest MailHog binary
go install github.com/mailhog/MailHog@latest

# Or download directly
wget https://github.com/mailhog/MailHog/releases/latest/download/MailHog_linux_amd64
chmod +x MailHog_linux_amd64
sudo mv MailHog_linux_amd64 /usr/local/bin/mailhog
```

### Option 2: Docker Setup

```bash
# Using Docker
docker run -d -p 1025:1025 -p 8025:8025 mailhog/mailhog

# Using Docker Compose (included)
docker-compose up -d mailhog
```

## Usage

### Basic Commands

```bash
# Start MailHog with default settings
mailhog

# Custom ports
mailhog -smtp-bind-addr :1025 -ui-bind-addr :8025

# Background execution
mailhog &

# Stop MailHog
pkill mailhog
```

### Configuration Options

#### Storage Options

```bash
# Memory storage (default, ephemeral)
mailhog -storage memory

# MongoDB storage (persistent)
mailhog -storage mongodb -mongo-uri 127.0.0.1:27017 -mongo-db mailhog

# Maildir storage (file-based)
mailhog -storage maildir -maildir-path ./mail_storage
```

#### Network Configuration

```bash
# Bind to all interfaces
mailhog -smtp-bind-addr 0.0.0.0:1025 -ui-bind-addr 0.0.0.0:8025

# Custom hostname
mailhog -hostname mailhog.test.local

# CORS configuration
mailhog -cors-origin "http://localhost:3000,http://localhost:5173"
```

#### Authentication

```bash
# Create auth file
echo "admin:$(bcrypt-hash 'password123')" > auth_file.txt

# Enable authentication
mailhog -auth-file auth_file.txt
```

### Framework Integration

#### Node.js with Nodemailer

```javascript
const transporter = nodemailer.createTransporter({
  host: 'localhost',
  port: 1025,
  secure: false,
  auth: false,
  tls: {
    rejectUnauthorized: false
  }
});

const mailOptions = {
  from: 'test@example.com',
  to: 'recipient@example.com',
  subject: 'Test Email',
  text: 'This is a test email sent via MailHog'
};

transporter.sendMail(mailOptions);
```

#### Python SMTP

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Create SMTP connection
server = smtplib.SMTP('localhost', 1025)
server.starttls()

# Create message
msg = MIMEMultipart()
msg['From'] = 'test@example.com'
msg['To'] = 'recipient@example.com'
msg['Subject'] = 'Test Email'

# Add body
msg.attach(MIMEText('This is a test email sent via MailHog', 'plain'))

# Send email
server.send_message(msg)
server.quit()
```

#### PHPMailer

```php
$mail = new PHPMailer();
$mail->isSMTP();
$mail->Host = 'localhost';
$mail->Port = 1025;
$mail->SMTPSecure = false;
$mail->SMTPAuth = false;

$mail->setFrom('test@example.com', 'Test Sender');
$mail->addAddress('recipient@example.com');

$mail->Subject = 'Test Email';
$mail->Body = 'This is a test email sent via MailHog';

$mail->send();
```

## API Usage

### REST API Endpoints

```bash
# Get all messages
curl http://localhost:8025/api/v1/messages

# Get specific message
curl http://localhost:8025/api/v1/messages/{message-id}

# Search messages
curl -X POST http://localhost:8025/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "subject:test"}'

# Delete all messages
curl -X DELETE http://localhost:8025/api/v1/messages

# Get message count
curl http://localhost:8025/api/v1/messages?limit=1 | jq '.total'
```

### JavaScript API Example

```javascript
// Fetch messages from MailHog API
async function getMessages() {
  const response = await fetch('http://localhost:8025/api/v1/messages');
  const data = await response.json();
  return data.items;
}

// Send search query
async function searchMessages(query) {
  const response = await fetch('http://localhost:8025/api/v1/search', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  return response.json();
}
```

## Docker Integration

### Basic Docker Setup

```yaml
# docker-compose.yml
version: '3.8'
services:
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"  # SMTP port
      - "8025:8025"  # UI/API port
    environment:
      - MH_HOSTNAME=mailhog.docker.local
      - MH_SMTP_BIND_ADDR=0.0.0.0:1025
      - MH_UI_BIND_ADDR=0.0.0.0:8025
    restart: unless-stopped
```

### Full Development Stack

```yaml
version: '3.8'
services:
  mailhog:
    image: mailhog/mailhog:latest
    ports:
      - "1025:1025"
      - "8025:8025"
    environment:
      - MH_HOSTNAME=mailhog.docker.local
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8025/api/v1/status"]
      interval: 30s
      timeout: 10s
      retries: 3

  app:
    build: .
    environment:
      - SMTP_HOST=mailhog
      - SMTP_PORT=1025
    depends_on:
      - mailhog
```

## Testing

### Automated Email Testing

```bash
# Run comprehensive email test suite
./scripts/test_email_workflow.sh --config test_config.json

# Send single test email
./scripts/send_test_email.sh --to test@example.com --subject "Test" --body "Content"

# Bulk email testing
./scripts/mailhog_manager.sh --bulk-send --count 100 --to test@example.com
```

### Integration Testing

```javascript
// Jest test example
describe('Email Service', () => {
  beforeEach(async () => {
    // Clear all messages before each test
    await fetch('http://localhost:8025/api/v1/messages', {
      method: 'DELETE'
    });
  });

  test('should send welcome email', async () => {
    // Send email through your application
    await emailService.sendWelcomeEmail('test@example.com');

    // Verify email was captured by MailHog
    const response = await fetch('http://localhost:8025/api/v1/messages');
    const data = await response.json();

    expect(data.items).toHaveLength(1);
    expect(data.items[0].Content.Headers.Subject[0]).toBe('Welcome!');
  });
});
```

## Scripts and Utilities

The plugin includes several utility scripts:

- **`scripts/mailhog_manager.sh`** - Complete MailHog server management
- **`scripts/send_test_email.sh`** - Send test emails via SMTP
- **`scripts/test_email_workflow.sh`** - Automated testing workflow

### Using the Scripts

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Server management
./scripts/mailhog_manager.sh start
./scripts/mailhog_manager.sh status
./scripts/mailhog_manager.sh stop

# Send test emails
./scripts/send_test_email.sh \
  --to test@example.com \
  --subject "Test Email" \
  --body "This is a test message" \
  --from sender@example.com
```

## Advanced Features

### Network Simulation (Jim)

Enable chaotic network testing to simulate real-world conditions:

```bash
# Enable Jim with default settings
mailhog -invite-jim

# Custom Jim configuration
mailhog -invite-jim \
  -jim-accept 0.95 \
  -jim-reject-sender 0.1 \
  -jim-reject-recipient 0.1 \
  -jim-disconnect 0.02 \
  -jim-linkspeed-affect 0.2
```

### Outgoing SMTP Configuration

Configure MailHog to forward emails to a real SMTP server:

```json
{
  "server": "smtp.gmail.com",
  "port": 587,
  "username": "your-email@gmail.com",
  "password": "app-specific-password",
  "tls": true,
  "from": "your-email@gmail.com"
}
```

```bash
mailhog -outgoing-smtp outgoing_config.json
```

### Performance Optimization

For high-volume testing scenarios:

```bash
# MongoDB with indexing for performance
mailhog \
  -storage mongodb \
  -mongo-uri mongodb://localhost:27017/mailhog_perf \
  -mongo-db mailhog_perf \
  -mongo-coll messages
```

```javascript
// Create MongoDB indexes for better performance
db.messages.createIndex({ "created": -1 });
db.messages.createIndex({ "From": 1 });
db.messages.createIndex({ "To.Address": 1 });
```

## Configuration Files

### Application Configuration Examples

The plugin includes ready-to-use configuration files for popular frameworks:

- **`examples/app-configs/nodemailer.js`** - Node.js/Nodemailer setup
- **`examples/app-configs/python-smtp.py`** - Python SMTP configuration
- **`examples/docker-compose.yml`** - Docker Compose setup

### Reference Documentation

- **`references/configurations.md`** - Advanced configuration examples
- **`references/api-endpoints.md`** - Complete API reference
- **`references/integration-patterns.md`** - Framework integration guides

## Troubleshooting

### Common Issues

**Port Conflicts:**
```bash
# Check what's using the ports
lsof -i :1025 -i :8025

# Kill processes if needed
kill -9 <PID>
```

**MailHog Not Starting:**
```bash
# Check if MailHog is installed
which mailhog

# Start with verbose logging
mailhog -v
```

**Emails Not Appearing:**
```bash
# Test SMTP connection manually
telnet localhost 1025

# Check MailHog status
curl http://localhost:8025/api/v1/status
```

### Health Check Script

```bash
#!/bin/bash
# health_check.sh

echo "Checking MailHog health..."

# Check SMTP port
if telnet localhost 1025 <<< "QUIT" > /dev/null 2>&1; then
    echo "✓ SMTP port 1025 is accessible"
else
    echo "✗ SMTP port 1025 is not accessible"
fi

# Check UI/API port
if curl -s http://localhost:8025 > /dev/null; then
    echo "✓ UI/API port 8025 is accessible"
else
    echo "✗ UI/API port 8025 is not accessible"
fi

# Check API status
if curl -s http://localhost:8025/api/v1/status > /dev/null; then
    echo "✓ API is responding"
else
    echo "✗ API is not responding"
fi
```

## Security Considerations

- **Never expose MailHog directly to the internet without authentication**
- **Use authentication in production environments**
- **Captured emails may contain sensitive information**
- **Regularly clean up stored messages in production**
- **Use secure passwords for auth files**
- **Configure firewall rules to limit access**

## Environment Variables

MailHog supports configuration via environment variables:

```bash
# Environment variable naming: MH_<FLAG_NAME_IN_UPPERCASE>
export MH_SMTP_BIND_ADDR=0.0.0.0:1025
export MH_UI_BIND_ADDR=0.0.0.0:8025
export MH_HOSTNAME=mailhog.env.local
export MH_STORAGE=mongodb
export MH_MONGO_URI=mongodb://localhost:27017/mailhog
export MH_MONGO_DB=mailhog
export MH_MONGO_COLL=messages
export MH_CORS_ORIGIN="http://localhost:3000"

# Run with environment variables
mailhog
```

## Plugin Structure

```
mailhog-plugin/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/
│   └── mailhog/
│       ├── SKILL.md         # Main skill documentation
│       ├── scripts/         # Utility scripts
│       │   ├── mailhog_manager.sh
│       │   ├── send_test_email.sh
│       │   └── test_email_workflow.sh
│       ├── examples/        # Configuration examples
│       │   ├── app-configs/
│       │   └── docker-compose.yml
│       └── references/      # Reference documentation
│           ├── configurations.md
│           ├── api-endpoints.md
│           └── integration-patterns.md
└── README.md                # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions:

- GitHub Issues: [Repository Issues](https://github.com/Whamp/marketplace/issues)
- MailHog Documentation: [Official MailHog Docs](https://github.com/mailhog/MailHog)

## Related Plugins

Check out other development plugins in the marketplace:

- **PocketBase Plugin** - Backend-as-a-service development toolkit
- **Testing Plugins** - Additional testing and validation tools
- **Development Tools** - More development productivity plugins