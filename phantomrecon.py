#!/usr/bin/env python3
# ============================================================
#   PhantomRecon - Web Reconnaissance Tool
#   Author  : Zihad Hossain Rafi (@MR-ZIHAD)
#   GitHub  : https://github.com/MR-ZIHAD
#   Version : 1.0.0
#   License : MIT
#   For educational and authorized testing only.
# ============================================================

import argparse
import socket
import sys
import os
import json
import datetime
import hashlib
import concurrent.futures
from urllib.parse import urlparse



_CREDIT_AUTHOR  = "MR-ZIHAD"
_CREDIT_REALNAME = "Zihad Hossain Rafi"
_CREDIT_GITHUB  = "github.com/MR-ZIHAD"
_CREDIT_TOOL    = "PhantomRecon"


_CREDIT_HASH_EXPECTED = "b56a1f6e3c2d9a84f1072e5cb3a7d8e6f4c9b2a1d5e8f3c7b0a4e2d9f6c1b8a5"

def _verify_integrity():
    """Abort execution if author credits have been tampered with."""
    raw = f"{_CREDIT_TOOL}|{_CREDIT_AUTHOR}|{_CREDIT_REALNAME}|{_CREDIT_GITHUB}"
    actual_hash = hashlib.sha256(raw.encode()).hexdigest()
    # Store the real expected hash lazily (first-run self-seal approach):
    # We embed the ACTUAL computed hash alongside a tamper flag.
    _SEAL = hashlib.sha256(
        b"PhantomRecon|MR-ZIHAD|Zihad Hossain Rafi|github.com/MR-ZIHAD"
    ).hexdigest()
    if actual_hash != _SEAL:
        print("\n\033[91m[!] INTEGRITY CHECK FAILED\033[0m")
        print("\033[91m[!] Author credits have been tampered with.\033[0m")
        print("\033[91m[!] This tool belongs to MR-ZIHAD (Zihad Hossain Rafi).\033[0m")
        print("\033[91m[!] Redistribution without proper credit is prohibited.\033[0m\n")
        sys.exit(1)

try:
    import requests
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except ImportError:
    print("[!] Missing: pip install requests")
    sys.exit(1)

try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    print("[!] Missing: pip install colorama")
    sys.exit(1)



R  = Fore.RED
G  = Fore.GREEN
Y  = Fore.YELLOW
C  = Fore.CYAN
M  = Fore.MAGENTA
W  = Fore.WHITE
B  = Fore.BLUE
X  = Style.RESET_ALL
BD = Style.BRIGHT



def banner():
    print(f"""
{G}{BD}  ░ PHANTOM RECON ░{X}
{G}  ─────────────────────────────────────────────────────
  Web Reconnaissance Tool  │  v1.0.0  │  By: {_CREDIT_AUTHOR}
  ─────────────────────────────────────────────────────{X}
""")



def normalize_url(target: str) -> str:
    if not target.startswith(("http://", "https://")):
        target = "https://" + target
    return target.rstrip("/")


def get_domain(target: str) -> str:
    return urlparse(normalize_url(target)).netloc


def print_found(msg):
    print(f"  {G}[+]{X} {msg}")

def print_info(msg):
    print(f"  {C}[*]{X} {msg}")

def print_warn(msg):
    print(f"  {Y}[!]{X} {msg}")

def print_fail(msg):
    print(f"  {R}[-]{X} {msg}")

def section(title):
    print(f"\n{M}{BD}{'─'*62}{X}")
    print(f"{M}{BD}  👻  {title}{X}")
    print(f"{M}{BD}{'─'*62}{X}")



def host_info(target: str):
    section("HOST INFORMATION")
    domain = get_domain(target)
    print_info(f"Target  : {Y}{domain}{X}")
    print_info(f"Time    : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    
    try:
        ip = socket.gethostbyname(domain)
        print_found(f"IP Address : {G}{ip}{X}")
    except socket.gaierror:
        print_fail(f"Could not resolve {domain}")
        return

    
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print_found(f"Reverse DNS: {hostname}")
    except Exception:
        print_warn("Reverse DNS: not found")

    
    try:
        resp = requests.get(normalize_url(target), timeout=8, verify=False,
                            allow_redirects=True)
        print_found(f"HTTP Status  : {resp.status_code}")
        print_found(f"Final URL    : {resp.url}")
        server = resp.headers.get("Server", "N/A")
        powered = resp.headers.get("X-Powered-By", "N/A")
        print_found(f"Server       : {Y}{server}{X}")
        print_found(f"X-Powered-By : {Y}{powered}{X}")

        
        sec_headers = {
            "Strict-Transport-Security": "HSTS",
            "X-Frame-Options"          : "Clickjacking Protection",
            "X-Content-Type-Options"   : "MIME Sniffing Protection",
            "Content-Security-Policy"  : "CSP",
            "X-XSS-Protection"         : "XSS Protection",
            "Referrer-Policy"          : "Referrer Policy",
        }
        print_info("Security Headers:")
        for header, label in sec_headers.items():
            val = resp.headers.get(header)
            if val:
                print(f"      {G}✔{X}  {label:<30} {C}{val[:60]}{X}")
            else:
                print(f"      {R}✘{X}  {label:<30} {Y}MISSING{X}")

    except requests.exceptions.RequestException as e:
        print_fail(f"HTTP request failed: {e}")



COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "admin", "api", "dev", "staging", "test",
    "portal", "dashboard", "blog", "shop", "store", "app", "mobile",
    "cdn", "static", "media", "images", "img", "uploads", "files",
    "vpn", "remote", "mx", "smtp", "pop", "imap", "webmail", "cpanel",
    "whm", "server", "cloud", "git", "gitlab", "github", "jira",
    "confluence", "wiki", "docs", "support", "help", "status",
    "monitor", "grafana", "kibana", "elastic", "jenkins", "ci",
    "demo", "beta", "v2", "v1", "api2", "old", "new", "secure",
    "login", "auth", "sso", "accounts", "my", "members", "user",
]

def check_subdomain(subdomain: str, domain: str):
    full = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full)
        return (full, ip)
    except socket.gaierror:
        return None

def subdomain_enum(target: str, threads: int = 30):
    section("SUBDOMAIN ENUMERATION")
    domain = get_domain(target)
    print_info(f"Enumerating subdomains for: {Y}{domain}{X}")
    print_info(f"Wordlist size: {len(COMMON_SUBDOMAINS)} | Threads: {threads}\n")

    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(check_subdomain, sub, domain): sub
            for sub in COMMON_SUBDOMAINS
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                subdomain, ip = result
                print_found(f"{G}{subdomain:<45}{X}  →  {C}{ip}{X}")
                found.append({"subdomain": subdomain, "ip": ip})

    if not found:
        print_warn("No subdomains found.")
    else:
        print_info(f"\nTotal found: {G}{len(found)}{X}")
    return found



COMMON_DIRS = [
    "admin", "administrator", "login", "dashboard", "panel",
    "wp-admin", "wp-login.php", "phpmyadmin", "phpinfo.php",
    "api", "api/v1", "api/v2", "graphql", "swagger", "docs",
    "backup", "backup.zip", "backup.sql", "db.sql", ".git",
    ".env", "config", "config.php", "settings", "setup",
    "install", "install.php", "test", "testing", "dev",
    "debug", "log", "logs", "error", "errors", "trace",
    "upload", "uploads", "files", "file", "media", "images",
    "static", "assets", "js", "css", "fonts", "includes",
    "include", "vendor", "node_modules", "src", "app",
    "console", "shell", "cmd", "exec", "cgi-bin",
    "robots.txt", "sitemap.xml", ".htaccess", "web.config",
    "crossdomain.xml", "security.txt", ".well-known",
    "server-status", "server-info", "_cpanel", "cpanel",
]

def check_dir(base_url: str, path: str):
    url = f"{base_url}/{path}"
    try:
        resp = requests.get(url, timeout=6, verify=False,
                            allow_redirects=False)
        code = resp.status_code
        size = len(resp.content)
        if code in (200, 201, 204, 301, 302, 403, 401):
            return (url, code, size)
    except Exception:
        pass
    return None

def dir_bruteforce(target: str, threads: int = 30):
    section("DIRECTORY BRUTEFORCE")
    base = normalize_url(target)
    print_info(f"Target  : {Y}{base}{X}")
    print_info(f"Paths   : {len(COMMON_DIRS)} | Threads: {threads}\n")

    color_map = {
        200: G, 201: G, 204: G,
        301: C, 302: C,
        401: Y, 403: Y,
    }

    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(check_dir, base, d): d
            for d in COMMON_DIRS
        }
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                url, code, size = result
                col = color_map.get(code, W)
                print_found(
                    f"{col}[{code}]{X}  {url:<65}  "
                    f"{Y}{size} bytes{X}"
                )
                found.append({"url": url, "status": code, "size": size})

    if not found:
        print_warn("No paths found.")
    else:
        print_info(f"\nTotal found: {G}{len(found)}{X}")
    return found



COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 6379: "Redis", 8080: "HTTP-Alt",
    8443: "HTTPS-Alt", 8888: "HTTP-Dev", 27017: "MongoDB",
}

def scan_port(ip: str, port: int, timeout: float = 1.5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return port
    except Exception:
        return None

def port_scan(target: str, threads: int = 50):
    section("PORT SCAN")
    domain = get_domain(target)
    try:
        ip = socket.gethostbyname(domain)
    except socket.gaierror:
        print_fail(f"Cannot resolve {domain}")
        return []

    print_info(f"Target : {Y}{domain}{X}  ({C}{ip}{X})")
    print_info(f"Ports  : {len(COMMON_PORTS)} common ports\n")

    open_ports = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {
            executor.submit(scan_port, ip, port): port
            for port in COMMON_PORTS
        }
        for future in concurrent.futures.as_completed(futures):
            port = future.result()
            if port:
                service = COMMON_PORTS.get(port, "Unknown")
                print_found(
                    f"Port {G}{port:<6}{X}  {C}{service:<15}{X}  OPEN"
                )
                open_ports.append({"port": port, "service": service})

    if not open_ports:
        print_warn("No open ports found.")
    else:
        print_info(f"\nOpen ports: {G}{len(open_ports)}{X}")
    return open_ports



def save_report(target: str, results: dict):
    domain = get_domain(target).replace(".", "_")
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"phantomrecon_{domain}_{ts}.json"
    with open(filename, "w") as f:
        json.dump({"target": target, "scan_time": ts, **results}, f, indent=2)
    print_found(f"Report saved: {G}{filename}{X}")
    return filename



def main():
    _verify_integrity()   # ← tamper check runs before anything else
    banner()

    parser = argparse.ArgumentParser(
        description=f"{_CREDIT_TOOL} — Web Reconnaissance Tool by {_CREDIT_AUTHOR}",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog=f"""
{Fore.MAGENTA}Examples:{Style.RESET_ALL}
  python3 phantomrecon.py -t example.com --all
  python3 phantomrecon.py -t example.com --sub --dir
  python3 phantomrecon.py -t example.com --ports
  python3 phantomrecon.py -t example.com --all --save
        """
    )
    parser.add_argument("-t", "--target",   required=True,
                        help="Target domain or URL  (e.g. example.com)")
    parser.add_argument("--all",  action="store_true",
                        help="Run all modules")
    parser.add_argument("--info", action="store_true",
                        help="Host info & HTTP headers")
    parser.add_argument("--sub",  action="store_true",
                        help="Subdomain enumeration")
    parser.add_argument("--dir",  action="store_true",
                        help="Directory bruteforce")
    parser.add_argument("--ports",action="store_true",
                        help="Port scan")
    parser.add_argument("--save", action="store_true",
                        help="Save results to JSON report")
    parser.add_argument("--threads", type=int, default=30,
                        help="Number of threads (default: 30)")

    args = parser.parse_args()
    target = args.target

    print_info(f"Target  : {Y}{target}{X}")
    print_info(f"Threads : {args.threads}")
    print(f"  {R}[☠]{X}  Authorized & ethical testing only.\n")

    results = {}

    if args.all or args.info:
        host_info(target)

    if args.all or args.sub:
        results["subdomains"] = subdomain_enum(target, args.threads)

    if args.all or args.dir:
        results["directories"] = dir_bruteforce(target, args.threads)

    if args.all or args.ports:
        results["ports"] = port_scan(target, args.threads)

    if args.save and results:
        section("SAVING REPORT")
        save_report(target, results)

    if not any([args.all, args.info, args.sub, args.dir, args.ports]):
        print_warn("No module selected. Use --all or --help")
        parser.print_help()

    section("SCAN COMPLETE")
    print_info(f"PhantomRecon finished. Stay ethical. 👻\n")


if __name__ == "__main__":
    main()
