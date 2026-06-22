from integration import run_scan_and_report

if __name__ == "__main__":
    print("=" * 50)
    print("SentinelPy — Advanced Port Scanner")
    print("=" * 50)

    SCAN_ID = int(input("Enter scan_id from backend: "))
    TARGET = input("Enter target IP or hostname: ")
    PORT_INPUT = input("Enter ports (comma separated) or press Enter for defaults: ").strip()

    if PORT_INPUT:
        PORTS = [int(p.strip()) for p in PORT_INPUT.split(",")]
    else:
        PORTS = [21, 22, 23, 25, 53, 80, 443, 3306, 5432, 8080, 8443]

    run_scan_and_report(SCAN_ID, TARGET, PORTS)