# modules/cve_matcher.py

def match_vulnerability(service, version, vulnerability_db):
    """
    Match a service and version against the vulnerability database.

    Args:
        service (str): Service name (e.g. Apache, OpenSSH)
        version (str): Version number (e.g. 2.4.49)
        vulnerability_db (dict): Vulnerability database

    Returns:
        dict or None
    """

    # Check if service exists
    if service in vulnerability_db:

        # Check if version exists
        if version in vulnerability_db[service]:

            vulnerability = vulnerability_db[service][version]

            print("\n[!] Vulnerability Found!")
            print(f"Service     : {service}")
            print(f"Version     : {version}")
            print(f"CVE ID      : {vulnerability['cve']}")
            print(f"Severity    : {vulnerability['severity']}")
            print(f"Description : {vulnerability['description']}")

            return vulnerability

    return None


# Testing
if __name__ == "__main__":

    vulnerability_db = {
        "Apache": {
            "2.4.49": {
                "cve": "CVE-2021-41773",
                "severity": "CRITICAL",
                "description": "Path Traversal Vulnerability",
                "exploit_available": True
            }
        },

        "OpenSSH": {
            "8.2p1": {
                "cve": "CVE-2020-14145",
                "severity": "MEDIUM",
                "description": "Observable Discrepancy Attack",
                "exploit_available": False
            }
        }
    }

    # Test Apache
    match_vulnerability("Apache", "2.4.49", vulnerability_db)

    # Test OpenSSH
    match_vulnerability("OpenSSH", "8.2p1", vulnerability_db)