# Runbook — Disk Full

Checks:
- `df -h`
- `sudo du -sh /var/log/* 2>/dev/null | sort -h | tail`
- Look for runaway logs

Fix:
- Remove old logs/temp
- Enable log rotation
Prevention:
- Disk alerting, logrotate, retention policy.

