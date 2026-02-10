# Runbook — Service Down (Linux/systemd mindset)

Symptoms:
- "Connection refused" OR service not responding

Differentiate:
- Refused = host reachable but nothing listening / service down
- Timeout = network path / firewall / DNS / routing

Checks:
- `ss -lntp | head`
- `curl -v http://localhost:PORT`
- `docker compose ps`
- `docker logs <container> --tail=200`

Fix:
- Restart service/container
- Verify port binding + config

Escalate when:
- Repeated crash loops, data corruption, or unknown root cause.

