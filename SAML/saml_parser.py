import base64
import urllib.parse
import xml.dom.minidom
import sys

def analyze_saml(raw_payload):
    # Handle URL encoding if present
    if "%" in raw_payload:
        raw_payload = urllib.parse.unquote(raw_payload)
    
    # Decode Base64
    try:
        decoded_bytes = base64.b64decode(raw_payload)
        xml_content = decoded_bytes.decode('utf-8')
    except Exception as e:
        print(f"[-] Failed to decode Base64 payload: {e}")
        return

    print("[+] Successfully Decoded SAML Response")
    
    # Parse XML
    try:
        dom = xml.dom.minidom.parseString(xml_content)
    except Exception as e:
        print(f"[-] Failed to parse XML structure: {e}")
        return

    response_sig = dom.getElementsByTagName("saml2p:Response")[0].getElementsByTagName("ds:Signature")
    assertion_sig = dom.getElementsByTagName("saml2:Assertion")[0].getElementsByTagName("ds:Signature")
    
    try:
        name_id = dom.getElementsByTagName("saml2:NameID")[0].firstChild.data
    except Exception:
        print("[-] Could not isolate NameID element.")

    print(f"[*] Response Level Signed: {len(response_sig) > 0}")
    print(f"[*] Assertion Level Signed: {len(assertion_sig) > 0}")
    print(f"[*] Current Identity (NameID): {name_id}")

    return(dom.toprettyxml(indent="  "))

if __name__ == "__main__":
    saml_response = sys.argv[1] if len(sys.argv) > 1 else "USAGE: python saml_parser.py saml_response.txt"

    with open(saml_response, "r") as f:
        sample_payload = f.read().strip()
    
    xml_content = analyze_saml(sample_payload)

    with open("saml_decoded.xml", "w") as f:
        f.write(xml_content)
    print("[+] Decoded SAML response saved to saml_decoded.xml")