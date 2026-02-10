# Alert Playbook (NOC)

## 1) InstanceDown
Meaning: Prometheus cannot scrape a target (service down, network issue, container stopped).
Confirm:
- Prometheus targets page: http://localhost:9090/targets
- From WSL: `docker compose ps`
Fix:
- Restart the container: `docker compose restart node-exporter`
Prevention:
- Add uptime alerts + restart policy (later) + basic health checks.

## 2) HighCPUUsage
Meaning: sustained CPU saturation.
Confirm:
- `top` / `htop`
- `ps aux --sort=-%cpu | head`
- Check logs for busy loops / spikes
Fix:
- Restart culprit service if safe
- Reduce load / adjust configuration
Prevention:
- Set thresholds, limit resources, fix root cause.

## 3) LowDiskSpaceRoot
Meaning: root filesystem running out of space.
Confirm:
- `df -h`
- `sudo du -sh /* 2>/dev/null | sort -h | tail`
Fix:
- Delete old logs/temp, enable log rotation
Prevention:
- logrotate, monitor growth, increase disk if needed.

