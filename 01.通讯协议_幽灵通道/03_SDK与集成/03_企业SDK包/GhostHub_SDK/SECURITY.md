# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly.

**Please DO NOT file a public GitHub issue for security vulnerabilities.**

Instead, please send a detailed report to security@ghosthub.dev

We will respond within 48 hours and work with you to understand and address the issue promptly.

## Disclosure Process

1. Reporter submits vulnerability via email
2. Project team confirms receipt within 48 hours
3. Project team investigates and provides timeline
4. Fix is developed and tested
5. Coordinated disclosure with reporter
6. Public release of security advisory

## Security Features

Ghost Hub SDK includes:

- Input validation for all user inputs
- Rate limiting for API endpoints
- Sensitive data protection (masking/encryption)
- Authentication support (API keys, JWT)
- Secure protocol support (TLS for MQTT/WebSocket)
