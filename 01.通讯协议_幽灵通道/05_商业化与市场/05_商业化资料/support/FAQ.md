# Ghost Hub SDK FAQ

## General

### What is Ghost Hub SDK?
Ghost Hub SDK is an enterprise-grade AI workflow orchestration framework that provides intent parsing (Intention Bank), IoT device integration (No-UI Adapter), and multi-agent collaboration (Agent Federation) in a single, unified SDK.

### What programming languages are supported?
Currently Python (primary), with REST API available for any language.

### What is the licensing model?
- **Community**: Free, up to 5 agents, 10 devices
- **Professional**: $499/year, up to 50 agents, 500 devices
- **Enterprise**: Custom pricing, unlimited capacity

---

## Technical

### How does intent matching work?
The Intention Bank uses a combination of:
1. Pattern matching against template keywords
2. Semantic similarity scoring
3. Domain classification

Input is tokenized, matched against templates, and ranked by confidence score.

### What IoT protocols are supported?
- MQTT (publish/subscribe)
- HTTP/REST
- WebSocket
- CoAP (constrained devices)

### Can I create custom templates?
Yes! Professional and Enterprise tiers support custom templates. See the Template Index documentation.

### How do agents communicate?
Agents use the Agent Federation component with configurable routing strategies:
- Round Robin
- Load Balance
- Capability Match
- Affinity Based

---

## Deployment

### Can Ghost Hub SDK run on-premise?
Yes. Docker and Kubernetes deployment options are available for all tiers.

### What are the system requirements?
- Python 3.10+
- 2GB RAM minimum
- 1GB disk space
- Network access for cloud features

### Is there a cloud-hosted option?
Yes, the Professional and Enterprise tiers include managed cloud deployment.

---

## Security

### Is Ghost Hub SDK SOC 2 certified?
Enterprise tier includes SOC 2 Type II compliance. Community and Professional tiers follow SOC 2 best practices.

### How is data encrypted?
- TLS 1.3 for data in transit
- AES-256 for data at rest
- Customer-managed keys available (Enterprise)

### Can I use my own authentication?
Yes. Enterprise supports SSO, LDAP, SAML, and OAuth2 integration.

---

## Support

### What support is available?

| Tier | Support Channel | Response Time |
|------|-----------------|---------------|
| Community | Forum | Best effort |
| Professional | Email | <4 hours |
| Enterprise | Priority | <1 hour |

### Are there training resources?
Yes:
- Documentation: docs.ghosthub.dev
- Video tutorials: youtube.com/ghosthub
- Community forum: community.ghosthub.dev
- Professional training: Available for Enterprise

---

## Pricing

### Is there a free trial?
Community tier is free forever. Professional tier includes a 14-day trial.

### Can I switch tiers?
Yes, upgrades take effect immediately. Downgrades apply at next billing cycle.

### What payment methods are accepted?
Credit card, wire transfer, and purchase order (Enterprise).

---

## Integration

### Does Ghost Hub work with Airflow/Temporal?
Yes. Ghost Hub can complement existing workflow tools for AI-specific use cases.

### Can I import existing workflows?
Yes. Templates can be imported from JSON. Custom migration support available for Enterprise.

### Is there an API?
Yes. REST API available for all tiers with comprehensive documentation.

---

## Troubleshooting

### My intent isn't matching correctly
1. Check if you're using the correct domain filter
2. Add more specific patterns to custom templates
3. Provide more context in the input

### Device connection failing
1. Verify network connectivity
2. Check MQTT/HTTP credentials
3. Ensure broker is accessible
4. Review firewall settings

### Workflow running slowly
1. Check monitoring dashboard for bottlenecks
2. Enable caching for frequent operations
3. Batch device commands where possible
4. Contact support if issues persist

---

## Contact

- **Sales**: sales@ghosthub.dev
- **Support**: support@ghosthub.dev
- **Enterprise**: enterprise@ghosthub.dev
- **Documentation**: docs.ghosthub.dev
