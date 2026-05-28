# modules/version_detector.py

import re


def extract_version(banner):
    """
    Extract service name and version from a banner.

    Supported:
    - Apache
    - OpenSSH

    Returns:
        dict or None
    """

    if not banner:
        return None

    # Apache Example:
    # Apache/2.4.49
    apache_match = re.search(r"(Apache)/([\d\.]+)", banner, re.IGNORECASE)

    if apache_match:
        return {
            "service": apache_match.group(1),
            "version": apache_match.group(2)
        }

    # OpenSSH Example:
    # OpenSSH_8.2p1
    openssh_match = re.search(r"(OpenSSH)[_/]([\w\.]+)", banner, re.IGNORECASE)

    if openssh_match:
        return {
            "service": openssh_match.group(1),
            "version": openssh_match.group(2)
        }

    return None


# Testing
if __name__ == "__main__":

    apache_banner = "Server: Apache/2.4.49 (Unix)"
    ssh_banner = "SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.5"

    print(extract_version(apache_banner))
    print(extract_version(ssh_banner))