# Incident — DNS/Name resolution issue (drill)

## Impact
- Risk of monitoring or service checks failing due to name resolution problems (cannot resolve hostnames → timeouts / failed requests).
- In a real NOC scenario this can appear as: endpoints unreachable, package updates failing, scrape targets failing, or slow user experience.

## Detection
- Symptoms during drill: resolution errors / slow resolves (e.g., `could not resolve host`, long waits on DNS queries).
- Validation source: compare direct IP reachability vs hostname reachability.

## Evidence / Signals
Typical signals include:
- `nslookup` / `dig` returns SERVFAIL / NXDOMAIN / long response time
- `ping 8.8.8.8` works but `ping google.com` fails (DNS issue)
- App logs show `lookup ...: no such host` or timeouts during name resolution

## Checks performed
1) Confirm resolver config
- `cat /etc/resolv.conf`

2) Test DNS resolution
- `nslookup google.com`
- `dig google.com +short`

3) Differentiate DNS vs network path
- `ping 8.8.8.8`
- `ping google.com`

4) (Optional) Check latency / intermittent behavior
- repeat `dig` several times and compare response time

## Root cause (drill hypothesis)
- Resolver misconfiguration, unstable upstream resolver, or intermittent DNS failures leading to failed or slow hostname resolution.

## Resolution (Fix)
- Switch to a known good resolver temporarily (example), then retest:
  - update resolver config (environment dependent)
- Flush caches if relevant (depends on system)
- Re-run `nslookup/dig` and confirm hostname resolution is stable.

## Prevention / Follow-ups
- Document known-good resolvers and fallback plan
- Monitor DNS resolution time/health (alert on high latency / failures)
- Add a runbook step: always test IP vs hostname to isolate DNS quickly
