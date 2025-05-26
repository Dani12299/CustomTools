import sys
import socket

def probe_port(target, port):
    result = 1
    try:
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soc.settimeout(0.5)
        r = soc.connect_ex((target, port))
        if r == 0:
            result = r
        soc.close()
    except Exception as e:
        print(e)            # for debugging
        pass
    return result
    
def main():
    if len(sys.argv) < 2:
        print("Usage: python3 portscan.py <target>")
        
    target = sys.argv[1]
    open_ports = []
    ports = range(1, 1000)
    
    # Scan ports
    for port in ports:
        sys.stdout.flush()
        response = probe_port(target, port)
        if response == 0:
            open_ports.append(port)
    
    # Print result
    if open_ports:
        print("[*] Open Ports: ")
        print(sorted(open_ports))

if __name__ == "__main__":
    main()