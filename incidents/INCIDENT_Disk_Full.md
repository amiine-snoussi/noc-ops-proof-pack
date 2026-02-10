# Incident — Low disk space threshold drill (/mnt/c)

## Impact
- Risk of service failures due to low disk space (log writes failing, database write failures, containers misbehaving).
- On WSL2 setups, `/mnt/c` can be the first disk to fill (Windows host drive), affecting dev + lab environments.

## Detection
- Alert: `LowDiskSpaceMntC` (warning) — disk free < 15% on `/mnt/c` for 10 minutes (drill / threshold scenario)

## Checks performed
- Confirm usage:
  - `df -h`
- Identify top consumers:
  - `sudo du -sh /* 2>/dev/null | sort -h | tail`
  - if needed: `sudo du -sh /mnt/c/* 2>/dev/null | sort -h | tail`
- Check log growth:
  - `sudo du -sh /var/log/* 2>/dev/null | sort -h | tail`
- Check Docker footprint (common disk eater):
  - `docker system df`

## Likely root causes
- Runaway logs
- Large downloads / temp files
- Docker images/volumes buildup
- Unbounded cache directories

## Resolution plan (safe order)
1) Remove obvious temp files (safe targets only)
2) Rotate/clean old logs (keep recent logs)
3) Clean Docker artifacts (only if safe):
   - `docker image prune -f`
   - `docker system prune -f` (more aggressive)

## Prevention / Follow-ups
1) Keep disk alerting (`/` and `/mnt/c`)
2) Enforce log rotation + retention policy
3) Add periodic cleanup checklist (Docker + large dirs review)
