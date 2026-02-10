#!/usr/bin/env python3
import argparse
import socket
import time
import urllib.request

def check_dns(host: str, timeout: float = 2.0):
    socket.setdefaulttimeout(timeout)
    try:
        ip = socket.gethostbyname(host)
        return True, ip
    except Exception as e:
        return False, str(e)

def check_tcp(host: str, port: int, timeout: float = 2.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True, "open"
    except Exception as e:
        return False, str(e)

def check_http(url: str, timeout: float = 3.0):
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return True, f"HTTP {resp.status}"
    except Exception as e:
        return False, str(e)

def main():
    p = argparse.ArgumentParser(description="Simple NOC-style health check (DNS/TCP/HTTP).")
    p.add_argument("--dns", nargs="*", default=["google.com"], help="Domains to resolve")
    p.add_argument("--tcp", nargs="*", default=["localhost:3000","localhost:9090"], help="host:port targets")
    p.add_argument("--http", nargs="*", default=["http://localhost:3000","http://localhost:9090/-/ready"], help="URLs to GET")
    args = p.parse_args()

    print("=== HEALTHCHECK ===")
    print(time.strftime("UTC %Y-%m-%d %H:%M:%S", time.gmtime()))
    print()

    print("DNS checks:")
    for host in args.dns:
        ok, info = check_dns(host)
        print(f"- {host}: {'PASS' if ok else 'FAIL'} ({info})")
    print()

    print("TCP checks:")
    for target in args.tcp:
        host, port_s = target.split(":")
        ok, info = check_tcp(host, int(port_s))
        print(f"- {host}:{port_s}: {'PASS' if ok else 'FAIL'} ({info})")
    print()

    print("HTTP checks:")
    for url in args.http:
        ok, info = check_http(url)
        print(f"- {url}: {'PASS' if ok else 'FAIL'} ({info})")

if __name__ == "__main__":
    main()

