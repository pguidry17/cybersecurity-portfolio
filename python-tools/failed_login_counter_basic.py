#!/usr/bin/env python3

"""
failed_login_counter_basic.py
Author: P. Guid

A simple beginner-friendly script that counts how many failed SSH
login attempts exist in a Linux auth.log file.

Usage:
    python3 failed_login_counter_basic.py auth.log
"""

import sys

if len(sys.argv) != 2:
    print("Usage: python3 failed_login_counter_basic.py <auth.log>")
    sys.exit(1)

log_file = sys.argv[1]

failed_lines = []

try:
    with open(log_file, "r") as f:
        for line in f:
            if "Failed password" in line:
                failed_lines.append(line)
except FileNotFoundError:
    print(f"[!] File not found: {log_file}")
    sys.exit(1)

print("\n=== Basic Failed Login Counter ===\n")
print(f"Total failed login attempts: {len(failed_lines)}\n")

print("Example failed attempts (first 5):")
print("----------------------------------")

for line in failed_lines[:5]:
    print(line.strip())

print()
