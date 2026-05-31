# Ghost Hub SDK Docker Deployment Guide

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/ghost-hub/sdk.git
cd sdk

# 2. Start services
docker-compose up -d

# 3. Check status
docker-compose ps

# 4. View logs
docker-compose logs -f ghost-hub-sdk
```

## Accessing Services

| Service | URL | Credentials |
|---------|-----|-------------|
| REST API | http://localhost:8080 | - |
| MQTT Broker | mqtt://localhost:1883 | - |
| Prometheus | http://localhost:9090 | - |
| Grafana | http://localhost:3000 | admin/admin |

## Production Deployment

### 1. Configure License

```bash
# Copy license file
cp /path/to/license.json ./license.json
```

### 2. Environment Variables

```bash
export GHOST_HUB_LICENSE_KEY="GH-ENT-XXXX-XXXX"
export GHOST_HUB_LOG_LEVEL="INFO"
export REDIS_HOST="redis"
export REDIS_PORT="6379"
```

### 3. Capacity Planning

The current compose file starts one `ghost-hub-sdk` API container and does not define a
separate worker service. Add a dedicated worker service before using worker scaling
commands, or remove fixed `container_name` values before horizontally scaling API
replicas.

### 4. Enable TLS

```bash
# Generate certificates
openssl req -x509 -newkey rsa:4096 -nodes -keyout key.pem -out cert.pem -days 365

# Update configuration
```

## Monitoring

### Prometheus Metrics

```bash
# Access metrics
curl http://localhost:8080/metrics
```

### Key Metrics

- `ghost_hub_workflows_total` - Total workflows executed
- `ghost_hub_intent_matches` - Intent matching count
- `ghost_hub_device_commands` - Device commands sent
- `ghost_hub_agent_tasks` - Agent tasks distributed
- `ghost_hub_latency_seconds` - Operation latency

### Grafana Dashboard

1. Open Grafana at http://localhost:3000
2. Login with admin/admin
3. Add Prometheus data source: http://prometheus:9090
4. Import dashboard from `grafana/dashboard.json`

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs ghost-hub-sdk

# Rebuild image
docker-compose build --no-cache
```

### License validation fails

```bash
# Verify license file
cat license.json | jq .

# Check license manager
docker-compose exec ghost-hub-sdk python -c "from ghost_hub_sdk.license import LicenseManager; print(LicenseManager().get_status())"
```

### MQTT connection issues

```bash
# Test MQTT
docker-compose exec mqtt mosquitto_pub -t test -m "hello"

# Check broker logs
docker-compose logs mqtt
```

## Security

### Change Default Passwords

```bash
# Grafana
export GF_SECURITY_ADMIN_PASSWORD="your-secure-password"

# MQTT (disable anonymous)
echo "allow_anonymous false" >> mosquitto.conf
echo "password_file /mosquitto/config/pwfile" >> mosquitto.conf
```

### Network Isolation

Use Docker secrets for sensitive data:

```yaml
secrets:
  license_key:
    file: ./license_key.txt
```

## Backup

### Data Backup

```bash
# Backup volumes
docker-compose stop
docker run --rm -v ghosthub_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data
docker-compose start
```

## Uninstall

```bash
# Stop and remove
docker-compose down -v

# Remove images
docker rmi ghosthub/sdk:latest
```
