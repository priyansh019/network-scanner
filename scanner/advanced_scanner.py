import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import os
import time

# Advanced port Scanner
print("=" * 50)
print("Advanced Port Scanner")
print("=" * 50)

# User Input
target = input("Enter the target: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Hostname could not be resolved.")
    exit()

# Port Range Input
start = int(input("Enter the starting port number: "))
end = int(input("Enter the ending port number: "))

print("\n Target: ", target)
print("IP Address: ", target_ip)
print("Port Range: ", start, "-", end)

print("\n + Scanning ...\n")
print("-" * 50)

#creates a directory to save the scan results
if not os.path.exists("network-scanner/reports"):
    os.makedirs("network-scanner/reports")

report_path = "network-scanner/reports/reports.txt"

#clears the report file if it already exists
with open(report_path, "w") as file:
    file.write("Advanced Port Scanner Report\n")
    file.write("=" * 50 + "\n")
    file.write(f"Target: {target}\n")
    file.write(f"IP Address: {target_ip}\n")
    file.write(f"Port Range: {start} - {end}\n")
    file.write(f"Scan Time: {datetime.now()}\n")
    file.write("=" * 50 + "\n\n")

open_ports = []

def grab_banner(s, port):
    try:
        # HTTP Banner Grabbing
        if port == 80:
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n"
            s.send(request.encode())
        
            banner = s.recv(4096).decode(errors="ignore")

             #Extract only important lines
            for line in banner.splitlines():

                if "Server:" in line:
                    return line.strip()
            return "HTTP Service Detected"

        # Other services
        else:
            banner = s.recv(4096).decode(errors="ignore").strip()

            if banner:
                return banner
            else:
                return "No banner Received"    
        
    except Exception as e:
        return "Banner Error"
    
    # Service Fingerprinting

def identify_service(port, banner):
    banner = banner.lower()
    if "apache" in banner:
        return "Apache Web Server" 
    elif "openssh" in banner:
        return "OpenSSH Server"
    elif "ftp" in banner:
        return "FTP Server"
    elif "smtp" in banner:
        return "SMTP Server"
    elif port == 80:
        return "HTTP Server"
    elif port == 443:
        return "HTTPS Server"
    else:
        return "Unknown Service"
        
# Port Scanning Function
    
def scan_port(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        #timeout
        s.settimeout(1)

        result = s.connect_ex((target_ip, port))

        if result == 0:

            # Detect service
            try:
                service = socket.getservbyport(port)
            except:
                service = "Unknown Service"

            # Grab banner
            banner = grab_banner(s, port)

            # Fingerprint service
            fingerprint = identify_service(port, banner)

            output = f"""
========================================
PORT: {port}
SERVICE: {service}
FINGERPRINT: {fingerprint}
BANNER: {banner}
STATUS: OPEN
========================================
"""
            print (output)


            open_ports.append(port)

             # Save to report
            with open(report_path, "a") as file:
                file.write(output + "\n")
        s.close()
    except Exception as e:
        pass

# Start Timer

start_time = time.time()

# ThreadPool for concurrent scanning

ports = range(start, end + 1)

with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, ports)

# End Timer

end_time = time.time()

# Final output

print("-" * 50)

print("\n[+] Scan Completed!")
print(f"[+] Total Open Ports: {len(open_ports)}")
print(f"[+] Scan Duration: {round(end_time - start_time, 2)} seconds")
print(f"[+] Report saved to: {report_path}")

print("=" * 50)