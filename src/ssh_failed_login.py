#!/usr/bin/env python3

import re
import sys
from collections import Counter


def analyze_log(log_file):
    failed_ips = Counter()

    try:
        with open(log_file, "r", errors="ignore") as file:
            for line in file:

                # Only analyze failed SSH login attempts
                if "Failed password" not in line:
                    continue

                # Extract IPv4 address
                match = re.search(
                    r"from\s+(\d{1,3}(?:\.\d{1,3}){3})",
                    line
                )

                if match:
                    ip_address = match.group(1)
                    failed_ips[ip_address] += 1

    except FileNotFoundError:
        print(f"[!] Log file not found: {log_file}")
        sys.exit(1)

    except PermissionError:
        print(f"[!] Permission denied: {log_file}")
        print("[!] Try running the script with sudo.")
        sys.exit(1)

    return failed_ips


def display_results(failed_ips):
    print()
    print("=" * 50)
    print("       SSH FAILED LOGIN ANALYZER")
    print("=" * 50)

    if not failed_ips:
        print("\n[+] No failed SSH login attempts found.")
        return

    print(f"\n{'IP Address':<20} {'Attempts':>10}")
    print("-" * 32)

    for ip, count in failed_ips.most_common():
        print(f"{ip:<20} {count:>10}")

    print("\n[+] Analysis completed.")
    print("=" * 50)


def main():
    if len(sys.argv) != 2:
        print("Usage:")
        print(f"  sudo python3 {sys.argv[0]} /path/to/auth.log")
        sys.exit(1)

    log_file = sys.argv[1]

    failed_ips = analyze_log(log_file)

    display_results(failed_ips)


if __name__ == "__main__":
    main()
