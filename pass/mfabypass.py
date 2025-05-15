import requests

host = "http://10.10.169.218:1337/reset_password.php"

response = requests.get(host)
print(response)