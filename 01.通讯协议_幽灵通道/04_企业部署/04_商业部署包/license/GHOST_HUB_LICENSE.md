# Ghost Hub SDK License System

> Enterprise licensing and activation

---

## License Types

| Tier | Features | Price |
|------|----------|-------|
| **Community** | Basic usage, open source | Free |
| **Professional** | Full SDK, 1 year support | $499/year |
| **Enterprise** | Unlimited, SLA, priority support | Custom |

---

## License File Format

```json
{
  "license_id": "GH-ENT-XXXX-XXXX",
  "type": "enterprise",
  "issued_to": "Company Name",
  "valid_from": "2026-01-01",
  "valid_until": "2027-01-01",
  "max_agents": -1,
  "max_devices": -1,
  "features": ["intention_bank", "no_ui_adapter", "agent_federation"],
  "support_tier": "priority",
  "signature": "BASE64_SIGNATURE"
}
```

---

## License Activation

### Python API

```python
from ghost_hub_sdk.license import LicenseManager, LicenseType

# Activate license
manager = LicenseManager()
result = manager.activate(
    license_key="GH-PRO-XXXX-XXXX",
    company="My Company"
)

if result.success:
    print(f"License activated: {result.license_id}")
else:
    print(f"Activation failed: {result.error}")
```

### Environment Variables

```bash
export GHOST_HUB_LICENSE_KEY="GH-PRO-XXXX-XXXX"
export GHOST_HUB_LICENSE_FILE="/path/to/license.json"
```

---

## License Verification

```python
# Check license status
status = manager.get_status()

print(f"Type: {status.type}")
print(f"Valid: {status.is_valid}")
print(f"Expires: {status.valid_until}")
print(f"Agents: {status.max_agents}")
```

---

## Offline Activation

```python
# Generate activation request
request = manager.generate_activation_request()

# Save request file
with open("activation_request.txt", "w") as f:
    f.write(request)

# After receiving activation response
manager.activate_offline("activation_response.txt")
```

---

## License Enforcement

```python
# Feature gates
if manager.has_feature("agent_federation"):
    sdk = GhostHubSDK(GhostHubConfig(agent_federation_enabled=True))

# Agent limits
agents = manager.get_agent_limit()
# -1 = unlimited

# Device limits
devices = manager.get_device_limit()
# -1 = unlimited
```

---

## Renewal

```python
# Check for renewal
renewal = manager.check_renewal()
if renewal.available:
    print(f"Renewal price: ${renewal.price}")
    print(f"Discount: {renewal.discount}%")

# Renew
manager.renew(renewal_token)
```

---

## Support Levels

| Feature | Community | Professional | Enterprise |
|---------|-----------|--------------|------------|
| Documentation | ✓ | ✓ | ✓ |
| Community Support | ✓ | ✓ | ✓ |
| Email Support | - | ✓ | ✓ |
| Priority Support | - | - | ✓ |
| SLA | - | - | 99.9% |
| Custom Development | - | - | ✓ |
