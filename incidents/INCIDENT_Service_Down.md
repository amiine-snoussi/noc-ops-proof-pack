# Incident — InstanceDown (node-exporter scrape failed due to Docker DNS)

## Impact
- Loss of host metrics from `node-exporter` (reduced observability for CPU/RAM/Disk/Network dashboards).
- No direct production outage, but monitoring coverage was degraded while the target was DOWN.

## Detection
- Prometheus alert **InstanceDown** fired (rule: `up == 0` for 1 minute).

## Evidence
- Prometheus **Targets** page showed the `node` job in **DOWN** state.
- Scrape error message (key detail):
  - `dial tcp: lookup node-exporter on 127.0.0.11:53: server misbehaving`
- Interpretation: Prometheus could not resolve the service name `node-exporter` via Docker’s embedded DNS resolver (`127.0.0.11`), so scraping `/metrics` failed.

## Checks performed
1) Confirmed monitoring stack status:
   - `docker compose ps`
2) Confirmed target health in Prometheus:
   - `http://localhost:9090/targets`
3) Verified the failure was name-resolution/scrape related (Docker DNS):
   - Observed `lookup node-exporter on 127.0.0.11:53` in the scrape error.

## Resolution (Fix)
- Restarted the exporter / stack to restore service discovery and scraping:
  - `docker start noc_node_exporter`  (or `docker compose restart node-exporter`)
- Validated recovery:
  - Prometheus Targets shows `node-exporter:9100` **UP**
  - InstanceDown alert returned to **inactive**

## Root cause
- Temporary failure in scraping `node-exporter` caused by Docker service discovery / embedded DNS resolution error (`127.0.0.11`) for the hostname `node-exporter`.

## Prevention / Follow-ups
- Added/kept **restart policies** (e.g., `restart: unless-stopped`) to reduce downtime from transient failures.
- Updated runbook to include a **DNS/service discovery verification** step when a target is DOWN:
  - Check Prometheus Targets for `lookup ... 127.0.0.11:53` errors
  - Confirm container/network status with `docker compose ps`
- Keep the InstanceDown alert as a first-response signal for observability gaps.

