# Runbook — DNS Issue

Symptoms:
- Websites slow, "could not resolve host", intermittent timeouts

Checks:
- `cat /etc/resolv.conf`
- `nslookup google.com`
- `dig google.com +short`
- Compare: `ping 8.8.8.8` vs `ping google.com`

Fix:
- Change resolver (temporary), flush caches, correct config
Prevention:
- Monitor DNS latency, set reliable resolvers, document fallback.

