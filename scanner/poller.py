import time
import requests
import os
from dotenv import load_dotenv
from integration import run_scan_and_report, get_token, refresh_token

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "https://network-scanner-1-p3wn.onrender.com")
POLL_INTERVAL = 10  # seconds

def get_initiated_scans():
    """Fetch all scans with status initiated from backend."""
    try:
        token = get_token()
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(
            f"{BACKEND_URL}/api/v1/scan/history",
            params={"status": "initiated", "limit": 10},
            headers=headers
        )
        if response.status_code == 401:
            refresh_token()
            return get_initiated_scans()
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"[-] Failed to fetch scans: {e}")
        return []

def process_scan(scan):
    """Run scanner on a single scan record."""
    scan_id = scan["id"]
    target = scan["target"]

    # Parse ports from string "[22, 80, 443]"
    try:
        ports_raw = scan["ports"].strip("[]").split(",")
        ports = [int(p.strip()) for p in ports_raw if p.strip()]
    except Exception:
        ports = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443]

    print(f"\n[+] Auto-processing scan #{scan_id} → {target}")
    run_scan_and_report(scan_id, target, ports)

def poll():
    """Main polling loop."""
    print("=" * 50)
    print("SentinelPy — Auto Scanner Poller")
    print(f"Polling every {POLL_INTERVAL} seconds...")
    print("Press Ctrl+C to stop.")
    print("=" * 50)

    while True:
        try:
            print(f"\n[*] Checking for pending scans...")
            pending = get_initiated_scans()

            if pending:
                print(f"[+] Found {len(pending)} pending scan(s)")
                for scan in pending:
                    process_scan(scan)
            else:
                print(f"[*] No pending scans. Waiting {POLL_INTERVAL}s...")

        except KeyboardInterrupt:
            print("\n[*] Poller stopped.")
            break
        except Exception as e:
            print(f"[-] Poller error: {e}")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    poll()