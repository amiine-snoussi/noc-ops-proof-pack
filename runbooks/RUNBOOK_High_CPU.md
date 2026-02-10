# Runbook — High CPU

Checks:
- `top` / `htop`
- `uptime`
- `ps aux --sort=-%cpu | head`
- `docker stats`

Fix:
- Restart culprit (if safe)
- Reduce load, tune settings
Prevention:
- Alerts, capacity planning, remove noisy jobs.

