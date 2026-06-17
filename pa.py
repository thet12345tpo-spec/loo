import os
import re
import base64
import time
import requests
from urllib.parse import urlparse, parse_qs, urljoin

# Terminal Color Codes
bcyan = "\033[1;36m"
reset = "\033[0m"
white = "\033[0;37m"
bgreen = "\033[1;32m"
bred = "\033[1;31m"
yellow = "\033[0;33m"

r = "\033[1;31m"
g = "\033[1;32m"
w = "\033[0m"

TIMEOUT_SEC = 10

def show_banner():
    try:
        os.system('clear' if os.name == 'posix' else 'cls')
    except:
        pass
    print(f"{bcyan}")
    print(r"""  ____  _   _ _____ ___ _____ 
 |  _ \| | | |_ _|_ _| ____| ____|
 | |_) | | | || | | ||  _| |  _|  
 |  _ <| |_| || | | || |___| |___ 
 |_| \_\\___/|___|___|_____|_____|""")
    print(f"      ⚡ ALL RUIJIE HACK ⚡")
    print(f"      Telegram : @naymin126653/@Christmas4040")
    print(f"      [ MODE: REQUESTS SESSION ]")
    print(f"{reset}")

class RuijieLoginManager:
    def __init__(self):
        self.ip = None
        self.mac = None
        self.current_sid = None
        self.session = requests.Session()
        self.phone_number = "12345678901"

    def check_internet(self):
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        try:
            resp = self.session.get(test_url, timeout=5, allow_redirects=False)
            return resp.status_code == 204
        except:
            return False

    def auto_detect_gateway(self):
        test_url = "http://connectivitycheck.gstatic.com/generate_204"
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14)'}
        try:
            resp = self.session.get(test_url, headers=headers, timeout=5, allow_redirects=False)
            if resp.status_code in (301, 302):
                location = resp.headers.get('Location', '')
                parsed_url = urlparse(location)
                query_params = parse_qs(parsed_url.query)
                
                gw_addr = query_params.get('gw_address')
                if gw_addr: self.ip = gw_addr[0]
                
                mac = query_params.get('mac') or query_params.get('umac')
                if mac: self.mac = mac[0]
                
                return True
        except:
            pass
        return self.ip is not None

    def fetch_sid(self):
        if not self.ip: return None
        
        step1_url = "https://portal-as.ruijienetworks.com/auth/wifidogAuth/login/?gw_id=c4b25be7c214&gw_sn=H1U320M001153&gw_address=192.168.110.1&gw_port=2060&ip=192.168.110.24&mac=5e:81:22:0b:f0:74&slot_num=14&nasip=192.168.1.166&ssid=VLAN233&ustate=0&mac_req=1&url=http%3A%2F%2F192.168.0.1%2F&chap_id=%5C006&chap_challenge=%5C262%5C050%5C017%5C376%5C373%5C321%5C110%5C247%5C102%5C033%5C243%5C231%5C130%5C012%5C345%5C112"
        headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 14)'}
        
        try:
            r1 = self.session.get(step1_url, headers=headers, timeout=TIMEOUT_SEC)
            js_match = re.search(r"self\.location\.href\s*=\s*['\"]([^'\"]+)['\"]", r1.text)
            if not js_match: return None
            
            step2_url = urljoin("https://portal-as.ruijienetworks.com", js_match.group(1))
            r2 = self.session.get(step2_url, headers=headers, timeout=TIMEOUT_SEC, allow_redirects=False)
            
            if r2.status_code == 302:
                location = r2.headers.get('Location', '')
                sid = parse_qs(urlparse(location).query).get('sessionId')
                if sid:
                    self.current_sid = sid[0]
                    return self.current_sid
        except:
            pass
        return None

    def login_voucher(self, voucher):
        if not self.current_sid: self.fetch_sid()
        if not self.current_sid: return False

        post_url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
        data = {"accessCode": voucher, "sessionId": self.current_sid, "apiVersion": 1}
        headers = {
            "Content-Type": "application/json",
            "Referer": f"https://portal-as.ruijienetworks.com/download/static/maccauth/src/index.html?sessionId={self.current_sid}"
        }
        
        try:
            resp = self.session.post(post_url, json=data, headers=headers, timeout=TIMEOUT_SEC)
            return 'logonUrl' in resp.text
        except:
            return False

    def send_final_auth(self):
        if not self.ip or not self.current_sid: return False
        auth_url = f'http://{self.ip}:2060/wifidog/auth'
        params = {'token': self.current_sid, 'phoneNumber': self.phone_number}
        try:
            resp = self.session.get(auth_url, params=params, timeout=TIMEOUT_SEC)
            return resp.status_code == 200
        except:
            return False

def start():
    show_banner()
    voucher = input(f"\n{yellow} Enter Voucher Code : {reset}").strip()
    if not voucher: return

    manager = RuijieLoginManager()
    print(f"\n{bgreen}[ * ] Keep-Alive Monitoring Started (Requests Mode).{reset}")
    
    while True:
        try:
            if not manager.check_internet():
                print(f"{yellow}[!] Connection lost. Re-authenticating...{reset}")
                if manager.auto_detect_gateway():
                    if manager.login_voucher(voucher):
                        if manager.send_final_auth():
                            print(f"{g}[+] Re-connected Successfully!{reset}")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[!] Stopped by user.")
            break
        except Exception as e:
            time.sleep(5)

if __name__ == "__main__":
    start()
