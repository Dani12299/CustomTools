import concurrent.futures
import requests
import os
import sys

def check_directory(dir, host):
    url = f"http://{host}/{dir}.html"       # Extension need to be manually adjusted
    # print(f"[*] Trying: {url}")
    req = requests.get(url)
    if req.status_code == 404:
        pass
    else:
        print(f"\t[+] Found: {dir}, Status: {req.status_code}")

def enumerate_directories(host, dir_file):
    print("[*] Setting up threads...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:     # Threads can be changed if needed
        for dir in dir_file:
            executor.submit(check_directory, dir, host) 
    
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 direnum.py <domain> <wordlist>")
        sys.exit(1)

    host = sys.argv[1]
    wordlist = sys.argv[2]
    
    if not os.path.isfile(wordlist):
        print(f"[-] Wordlist file {wordlist} does not exist.")
        sys.exit(1)
        
    dir_file = []
    print("[*] Loading wordlist...")
    lines = open(wordlist, 'r').readlines()
    for line in lines:
        dir_file.append(line.strip())
        
    enumerate_directories(host, dir_file)
    
if __name__ == "__main__":
    main()
    