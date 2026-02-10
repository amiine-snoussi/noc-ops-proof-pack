# NOC / Ops Monitoring Lab (Prometheus + Grafana)

Local lab environment for monitoring + alerting + incident drills.

Runs well on Windows + WSL2 Ubuntu with Docker Desktop.

---

## Components
- Prometheus (metrics + alerting rules)
- Grafana (dashboards)
- Node Exporter (host metrics)
- Docker Compose (orchestration)

Ports:
- Grafana: http://localhost:3000 (admin/admin)
- Prometheus: http://localhost:9090
  - Targets: http://localhost:9090/targets
  - Alerts: http://localhost:9090/alerts

---

## Layout
- `monitoring/` — Prometheus + Grafana provisioning
- `runbooks/` — troubleshooting runbooks + alert playbook
- `incidents/` — incident-style writeups (drills)
- `scripts/` — health check + log triage scripts
- `assets/` — screenshots/evidence

---

## Quick start

Start:
```bash
docker compose up -d
docker compose ps
````

Stop:

```bash
docker compose down
```

---

## Alerts configured

* `InstanceDown`
* `HighCPUUsage`
* `LowDiskSpaceRoot`
* `LowDiskSpaceMntC`

---

## Evidence (screenshots)

![Host overview](assets/01_grafana_host_overview.png)
![Network](assets/02_grafana_network.png)
![Target health](assets/03_grafana_target_health.png)
![Prometheus targets](assets/04_prometheus_targets.png)
![Prometheus alerts](assets/05_prometheus_alerts.png)
![docker compose ps](assets/06_compose_ps.png)
![Incident drill: InstanceDown](assets/07_incident_instance_down.png)
![Disk risk: df -h](assets/08_incident_disk_low.png)

---

## Drills

### Drill A — InstanceDown

```bash
docker stop noc_node_exporter
# wait 1–2 minutes, check /targets and /alerts
docker start noc_node_exporter
```

### Drill B — Disk workflow

```bash
df -h
sudo du -sh /* 2>/dev/null | sort -h | tail
```

---

## Scripts

Health checks:

```bash
python3 scripts/healthcheck.py
python3 scripts/healthcheck.py --dns google.com github.com --tcp localhost:3000 localhost:9090 --http http://localhost:3000 http://localhost:9090/-/ready
```

Log triage:

```bash
python3 scripts/log_triage.py /path/to/logfile.log
python3 scripts/log_triage.py /path/to/logfile.log --top 30
python3 scripts/log_triage.py /path/to/logfile.log --patterns ERROR Exception timeout refused failed
```

---

## Troubleshooting (WSL2 bind-mount issues)

If a container restart fails with a bind-mount error:

```bash
docker compose down --remove-orphans
docker compose up -d --force-recreate
```

If still broken, reset WSL then retry (PowerShell):

```powershell
wsl --shutdown


