# Runbook — Timeout vs Refused

Timeout:
- Network path issue (routing, firewall, DNS, upstream down)

Refused:
- Host reachable but port closed / service down

Checks:
- `ping <host>`
- `traceroute <host>`
- `nc -vz <host> <port>` (port reachability)
- `curl -v http://<host>:<port>`

Fix:
- Timeout: check DNS/routes/firewall
- Refused: restart service, verify listener/port/config

