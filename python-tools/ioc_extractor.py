#!/usr/bin/env python3

"""
ioc_extractor.py
Author: P. Guid

Description:
    This script extracts common Indicators of Compromise (IOCs) from log files,
    including IP addresses, usernames, and suspicious commands. It outputs the
    results in JSON format for easy use in security tools.

Usage:
    python3 ioc_extractor.py <logfile>
"""

import sys
import re
import json
from collections import defaultdict

if len(sys.argv) != 2:
    print("Usage: python3 ioc_extractor.py <logfile>")
    sys.exit(1)

log_file = sys.argv[1]

# Regex patterns
IP_REGEX = r"\b\d{1,3}(?:\.\d{1,3}){3}\b"
USER_REGEX = r"Failed password for(?: invalid user)? (\S+)"
REVERSE_SHELL_REGEX = r"(nc|netcat).*\s-e\s"
SUSPICIOUS_COMMANDS = [
    "netcat",
    "nc ",
    "-e /bin/bash",
    "bash -i",
    " /dev/tcp/",
    "curl ",
    "wget "
]

ips = set()
users = defaultdict(int)
suspicious_hits = []
reverse_shells = []

try:
    with open(log_file, "r") as f:
        for line in f:
            # Extract IPs
            found_ips = re.findall(IP_REGEX, line)
            for ip in found_ips:
                ips.add(ip)

            # Extract usernames
            user_match = re.search(USER_REGEX, line)
            if user_match:
                user = user_match.group(1)
                users[user] += 1

            # Detect suspicious commands
            if any(sig in line for sig in SUSPICIOUS_COMMANDS):
                suspicious_hits.append(line.strip())

            # Detect reverse shells
            if re.search(REVERSE_SHELL_REGEX, line):
                reverse_shells.append(line.strip())

except FileNotFoundError:
    print(f"[!] File not found: {log_file}")
    sys.exit(1)

# Build IOC dictionary
ioc_output = {
    "unique_ips": sorted(list(ips)),
    "failed_logins_by_user": users,
    "suspicious_commands": suspicious_hits,
    "reverse_shell_activity": reverse_shells
}

# Print JSON output
print(json.dumps(ioc_output, indent=4))
