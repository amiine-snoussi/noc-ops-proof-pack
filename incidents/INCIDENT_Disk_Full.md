# Incident — Low disk space threshold drill

Impact:
- Risk of service failure due to low disk space (log writes, DB writes, container failures).

Detection:
- Alert: LowDiskSpaceRoot (warning) (drill / threshold scenario)

Checks performed:
- `df -h` to confirm filesystem usage
- `du -sh /* | sort -h | tail` to identify top consumers
- Checked `/var/log` growth and container logs

Likely root causes:
- Runaway logs, large temp files, unbounded docker images/volumes

Resolution plan:
- Remove old logs/temp files
- Enforce log rotation and retention
- Clean docker artifacts (images/volumes) when safe

Prevention actions:
1) Keep disk alerting + add inode alert later
2) Enable logrotate + retention policy
3) Add weekly housekeeping checklist

