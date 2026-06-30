import socket
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://network-scanner-1-p3wn.onrender.com")
SCANNER_EMAIL = os.getenv("SCANNER_EMAIL")
SCANNER_PASSWORD = os.getenv("SCANNER_PASSWORD")

if not SCANNER_EMAIL or not SCANNER_PASSWORD:
    raise Exception("SCANNER_EMAIL and SCANNER_PASSWORD must be set in .env file")

# Token cache — avoids logging in on every request
_token_cache = {"token": None}


# ─── Authentication ────────────────────────────────────────────────────────────

def get_token() -> str:
    """
    Get JWT token from backend.
    Uses cached token if available.
    Registers automatically if account doesn't exist yet.
    """
    if _token_cache["token"]:
        return _token_cache["token"]

    # Try login first
    response = requests.post(
        f"{BACKEND_URL}/api/v1/auth/login",
        json={"email": SCANNER_EMAIL, "password": SCANNER_PASSWORD}
    )

    # If login fails, register then login
    if response.status_code == 401:
        print("[*] Scanner account not found, registering...")
        requests.post(
            f"{BACKEND_URL}/api/v1/auth/register",
            json={"email": SCANNER_EMAIL, "password": SCANNER_PASSWORD}
        )
        response = requests.post(
            f"{BACKEND_URL}/api/v1/auth/login",
            json={"email": SCANNER_EMAIL, "password": SCANNER_PASSWORD}
        )

    if response.status_code == 200:
        token = response.json()["access_token"]
        _token_cache["token"] = token
        print("[+] Authenticated with backend successfully")
        return token
    else:
        raise Exception(f"[-] Backend authentication failed: {response.status_code} - {response.text}")


def refresh_token() -> str:
    """Force fetch a fresh token — called when token expires (401)."""
    _token_cache["token"] = None
    return get_token()


# ─── Port Scanner ──────────────────────────────────────────────────────────────

def grab_banner(s, port, target):
    """Grab service banner from open port."""
    try:
        if port == 80:
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            s.send(request.encode())
            banner = s.recv(4096).decode(errors="ignore")
            for line in banner.splitlines():
                if "Server:" in line:
                    return line.strip()
            return "HTTP Service Detected"
        else:
            banner = s.recv(4096).decode(errors="ignore").strip()
            return banner if banner else "No banner received"
    except Exception:
        return "Banner Error"


def identify_service(port, banner):
    """Fingerprint service from banner, falling back to a port-based guess."""
    banner = banner.lower().strip()

    if "apache" in banner:
        return "Apache"
    elif "nginx" in banner:
        return "Nginx"
    elif "openssh" in banner or "ssh" in banner:
        return "OpenSSH"
    elif "ftp" in banner:
        return "FTP"
    elif "smtp" in banner:
        return "SMTP"
    elif "mysql" in banner:
        return "MySQL"
    elif "postgresql" in banner or "postgres" in banner:
        return "PostgreSQL"
    elif "telnet" in banner:
        return "Telnet"

    # No banner match — fall back to a labeled guess, not a confirmed ID
    port_map = {
        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
        80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS",
        3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
        8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    }
    guess = port_map.get(port)
    return f"{guess} (assumed)" if guess else "Unknown"


def scan_single_port(args):
    """
    Scan a single port and return structured result.
    Returns None if port is closed.
    """
    target_ip, port, target, vulnerability_db = args
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.1)
        result = s.connect_ex((target_ip, port))

        if result == 0:
            try:
                service = socket.getservbyport(port)
            except Exception:
                service = "Unknown"

            banner = grab_banner(s, port, target)
            fingerprint = identify_service(port, banner)

            version = "Unknown"
            try:
                from modules.version_detector import extract_version
                version_info = extract_version(banner)
                if version_info:
                    version = version_info["version"]
            except ImportError:
                pass

            vulnerability = None
            risk = "low"
            try:
                from modules.cve_matcher import match_vulnerability
                from modules.risk_classifier import classify_risk
                vulnerability = match_vulnerability(fingerprint, version, vulnerability_db)
                if vulnerability:
                    risk = classify_risk(vulnerability["severity"]).lower()
            except ImportError:
                pass

            s.close()
            return {
                "port": port,
                "service": service,
                "fingerprint": fingerprint,
                "banner": banner,
                "version": version,
                "vulnerability": vulnerability,
                "risk": risk
            }

        s.close()
        return None

    except Exception:
        return None


# ─── Risk Calculator ───────────────────────────────────────────────────────────

def calculate_highest_risk(results: list) -> str:
    """Calculate the highest risk level across all open ports."""
    risk_order = ["low", "medium", "high", "critical",
                  "minor risk", "moderate risk", "dangerous",
                  "immediate action required"]

    highest = "low"
    for result in results:
        if result:
            risk = result.get("risk", "low").lower()
            if risk in risk_order:
                if risk_order.index(risk) > risk_order.index(highest):
                    highest = risk

    risk_map = {
        "minor risk": "low",
        "moderate risk": "medium",
        "dangerous": "high",
        "immediate action required": "critical"
    }
    return risk_map.get(highest, highest)


# ─── Backend Communication ─────────────────────────────────────────────────────

def send_results_to_backend(scan_id: int, open_ports: list, services: dict, risk_level: str):
    """Send scan results to backend API. Auto-refreshes token if expired."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "scan_id": scan_id,
        "open_ports": open_ports,
        "services": services,
        "risk_level": risk_level
    }

    response = requests.post(
        f"{BACKEND_URL}/api/v1/scan/{scan_id}/results",
        json=payload,
        headers=headers
    )

    if response.status_code == 401:
        print("[*] Token expired, refreshing...")
        token = refresh_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{BACKEND_URL}/api/v1/scan/{scan_id}/results",
            json=payload,
            headers=headers
        )

    if response.status_code == 200:
        print(f"[+] Scan {scan_id} results sent to backend successfully")
        return True
    else:
        print(f"[-] Failed to send results: {response.status_code} - {response.text}")
        return False


def update_scan_status(scan_id: int, status: str):
    """Update scan status in backend."""
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        requests.patch(
            f"{BACKEND_URL}/api/v1/scan/{scan_id}/status",
            json={"status": status},
            headers=headers
        )
        print(f"[*] Scan {scan_id} status updated to: {status}")
    except Exception as e:
        print(f"[-] Failed to update status: {e}")


# ─── Main Integration Function ─────────────────────────────────────────────────

def run_scan_and_report(scan_id: int, target: str, ports: list):
    """
    Run a full network scan and send results to backend API.

    Args:
        scan_id: ID of the scan record created by backend
        target:  IP address or hostname to scan
        ports:   List of port numbers to scan

    Usage:
        from integration import run_scan_and_report
        run_scan_and_report(scan_id=1, target="192.168.1.1", ports=[22, 80, 443])
    """
    print(f"\n[+] Starting scan for target: {target}")
    print(f"[+] Ports to scan: {ports}")
    print(f"[+] Scan ID: {scan_id}\n")

    # Resolve hostname to IP
    try:
        target_ip = socket.gethostbyname(target)
        print(f"[+] Resolved IP: {target_ip}")
    except socket.gaierror:
        print(f"[-] Could not resolve hostname: {target}")
        update_scan_status(scan_id, "failed")
        return

    # Load vulnerability database
    try:
        db_path = os.path.join(os.path.dirname(__file__), "databases/vulnerabilities.json")
        with open(db_path, "r") as f:
            vulnerability_db = json.load(f)
    except FileNotFoundError:
        print("[-] Vulnerability database not found, continuing without CVE matching")
        vulnerability_db = {}

    # Prepare args for concurrent scanning
    scan_args = [(target_ip, port, target, vulnerability_db) for port in ports]

    print(f"[+] Scanning {len(ports)} ports...\n")
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(scan_single_port, scan_args))

    # Process results
    open_ports = []
    services = {}

    for result in results:
        if result:
            port = result["port"]
            open_ports.append(port)
            services[str(port)] = result["fingerprint"]
            print(f"  [OPEN] Port {port} - {result['fingerprint']} - Risk: {result['risk']}")

    print(f"\n[+] Scan complete. Open ports found: {len(open_ports)}")

    risk_level = calculate_highest_risk(results)
    print(f"[+] Overall risk level: {risk_level}")

    print(f"\n[+] Sending results to backend...")
    send_results_to_backend(scan_id, open_ports, services, risk_level)


# ─── Manual Test ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("SentinelPy Scanner — Backend Integration")
    print("=" * 50)

    SCAN_ID = int(input("Enter scan_id from backend: "))
    TARGET = input("Enter target IP or hostname: ")
    PORT_INPUT = input("Enter ports (comma separated) or press Enter for defaults: ").strip()

    if PORT_INPUT:
        PORTS = [int(p.strip()) for p in PORT_INPUT.split(",")]
    else:
        PORTS = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443]

    run_scan_and_report(SCAN_ID, TARGET, PORTS)