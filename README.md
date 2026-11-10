<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0d0221,40:003d1a,80:00ff88,100:00cfff&height=180&section=header&text=PhantomRecon&fontSize=55&fontColor=ffffff&animation=fadeIn&fontAlignY=42&desc=Web+Reconnaissance+Tool+%F0%9F%91%BB&descSize=18&descColor=00ff88&descAlignY=65"/>

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d0221)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-00ff88?style=for-the-badge&labelColor=0d0221)](LICENSE)
[![Author](https://img.shields.io/badge/Author-MR--ZIHAD-00cfff?style=for-the-badge&logo=github&labelColor=0d0221)](https://github.com/MR-ZIHAD)
[![Country](https://img.shields.io/badge/Made_in-Bangladesh_🇧🇩-ff0080?style=for-the-badge&labelColor=0d0221)]()

**PhantomRecon** is a fast, all-in-one **web reconnaissance tool** for ethical hackers and bug bounty hunters.  
Gather host info, enumerate subdomains, brute-force directories, and scan ports — all in one command.

> ⚠️ **For authorized and ethical testing only. Always get written permission before scanning.**

</div>

---

## 🔥 Features

| Module | Flag | Description |
|--------|------|-------------|
| Host Info | `--info` | IP, reverse DNS, HTTP headers, security headers audit |
| Subdomain Enum | `--sub` | DNS brute-force with 60+ common subdomains, multithreaded |
| Directory Scan | `--dir` | 50+ common paths — admin panels, backups, configs, APIs |
| Port Scanner | `--ports` | 20 common ports — SSH, FTP, MySQL, Redis, RDP and more |
| JSON Report | `--save` | Export full results to a JSON file |
| Run All | `--all` | Execute every module at once |

---

##  Installation

```bash
git clone https://github.com/MR-ZIHAD/PhantomRecon.git
cd PhantomRecon
pip install -r requirements.txt
```

---

##  Usage

```bash

python3 phantomrecon.py -t example.com --all

python3 phantomrecon.py -t example.com --info --sub

python3 phantomrecon.py -t example.com --ports

python3 phantomrecon.py -t example.com --all --save

python3 phantomrecon.py -t example.com --all --threads 50
```

---

##  Preview

```
  ░ PHANTOM RECON ░
  ─────────────────────────────────────────────────────
  Web Reconnaissance Tool  │  v1.0.0  │  By: MR-ZIHAD
  ─────────────────────────────────────────────────────

  [*] Target  : hackthebox.com
  [*] Threads : 30

  ──────────────────────────────────────────────────────
  👻  HOST INFORMATION
  ──────────────────────────────────────────────────────
  [+] IP Address   : 104.26.10.117
  [+] HTTP Status  : 200
  [+] Server       : cloudflare
  [*] Security Headers:
      ✔  HSTS                     max-age=31536000
      ✔  Clickjacking Protection  DENY
      ✘  XSS Protection           MISSING

  ──────────────────────────────────────────────────────
  👻  SUBDOMAIN ENUMERATION
  ──────────────────────────────────────────────────────
  [+] www.hackthebox.com    →  104.26.10.117
  [+] api.hackthebox.com    →  104.26.10.119
  [+] app.hackthebox.com    →  104.26.10.120

  ──────────────────────────────────────────────────────
  👻  PORT SCAN
  ──────────────────────────────────────────────────────
  [+] Port 80    HTTP     OPEN
  [+] Port 443   HTTPS    OPEN
  [+] Port 22    SSH      OPEN
```

---

##  Options

```
-t, --target     Target domain or URL (required)
--all            Run all modules
--info           Host information & security headers
--sub            Subdomain enumeration
--dir            Directory bruteforce
--ports          Port scan
--save           Save JSON report
--threads N      Thread count (default: 30)
```

---

##  Legal Disclaimer

> This tool is intended for **authorized security testing and educational purposes only**.  
> The author is **not responsible** for any misuse or illegal activity.  
> **Always obtain written permission** before scanning any target.  
> Unauthorized scanning may be **illegal** in your country.

---

##  Author

<div align="center">

**Zihad Hossain Rafi**

[![GitHub](https://img.shields.io/badge/GitHub-MR--ZIHAD-00ff88?style=for-the-badge&logo=github&labelColor=0d0221)](https://github.com/MR-ZIHAD)
[![YouTube](https://img.shields.io/badge/YouTube-@zihad__hossain__rafi-ff0080?style=for-the-badge&logo=youtube&labelColor=0d0221)](https://www.youtube.com/@zihad_hossain_rafi)

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ff88,50:00cfff,100:0d0221&height=100&section=footer"/>

</div>
