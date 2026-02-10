#!/usr/bin/env python3
import argparse
import re
from collections import Counter, defaultdict
from datetime import datetime

DEFAULT_PATTERNS = [
    r"\bERROR\b",
    r"\bException\b",
    r"\bTraceback\b",
    r"\btimeout\b",
    r"\brefused\b",
    r"\bfailed\b",
]

def parse_args():
    p = argparse.ArgumentParser(description="Quick log triage: count common error patterns.")
    p.add_argument("path", help="Path to a log file")
    p.add_argument("--top", type=int, default=20, help="Top N lines/pattern hits")
    p.add_argument("--patterns", nargs="*", default=DEFAULT_PATTERNS, help="Regex patterns to match")
    return p.parse_args()

def main():
    args = parse_args()
    compiled = [re.compile(ptn, re.IGNORECASE) for ptn in args.patterns]

    hits_by_pattern = Counter()
    last_seen = defaultdict(lambda: None)
    top_lines = Counter()

    with open(args.path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line_stripped = line.strip()
            matched_any = False
            for rgx, raw in zip(compiled, args.patterns):
                if rgx.search(line_stripped):
                    matched_any = True
                    hits_by_pattern[raw] += 1
                    last_seen[raw] = datetime.utcnow().isoformat() + "Z"  # time of scan
            if matched_any:
                # count exact lines (useful to spot repeated identical errors)
                top_lines[line_stripped] += 1

    print("=== LOG TRIAGE SUMMARY ===")
    print(f"File: {args.path}")
    print("\nPattern hits:")
    for ptn, cnt in hits_by_pattern.most_common():
        print(f"- {ptn}: {cnt} (last_seen_scan={last_seen[ptn]})")

    print("\nTop repeated matched lines:")
    for line, cnt in top_lines.most_common(args.top):
        print(f"[{cnt}x] {line[:200]}")

if __name__ == "__main__":
    main()

