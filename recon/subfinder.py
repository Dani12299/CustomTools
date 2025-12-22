import concurrent.futures
import socket
import os
import sys

def check_subdomain(subdomain, domain):
    try:
        full_domain = f"{subdomain}.{domain}"
        ip = socket.gethostbyname(full_domain)
        return full_domain, ip
    except socket.gaierror:
        return None

def enumerate_subdomains(domain, subfile):
    found = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = [executor.submit(check_subdomain, sub, domain) for sub in subfile]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                found.append(result)
                print(f"[+] Found: {result[0]}")
    return found
    
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 subfinder.py <domain> <subfile>")
        sys.exit(1)

    domain = sys.argv[1]
    wordlist = sys.argv[2]
    
    if not os.path.isfile(wordlist):
        print(f"[-] Subdomain file {wordlist} does not exist.")
        sys.exit(1)
        
    subfile = []
    lines = open(wordlist, 'r').readlines()
    for line in lines:
        subfile.append(line.strip())
        
    enumerate_subdomains(domain, subfile)
    
if __name__ == "__main__":
    main()
    