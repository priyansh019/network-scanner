import socket
target = input("Enter the target IP address: ")
print("Scanning target: " + target)
start = input("Enter the starting port number: ")
end = input("Enter the ending port number: ")
for port in range(int(start), int(end) + 1):
    # Create a socket object
    # AF_INET is the address family for IPv4, and SOCK_STREAM is the socket type for TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Set a timeout for the connection attempt to avoid hanging
    s.settimeout(0.1)
    result = s.connect_ex((target, port))
    if result == 0:
        print("Port {} is open".format(port))
    else:
        print("Port {} is closed".format(port))
    s.close()
print("Scanning completed.")